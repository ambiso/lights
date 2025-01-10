// use std::{thread::sleep, time::Duration};

use std::{any::Any, collections::HashMap, hash::Hash, sync::Arc, time::Duration};

use axum_macros::debug_handler;
use bracket_color::{prelude::HSV, rgb::RGB};
use glam::{Mat3, Vec3};
use rs_ws281x::{ChannelBuilder, ControllerBuilder, StripType};

// fn main() -> ! {
//     // Construct a single channel controller. Note that the
//     // Controller is initialized by default and is cleaned up on drop

//         // for p in 0..255 {

//         //     let leds = controller.leds_mut(0);
//         //     for led in leds.iter_mut() {
//         //         *led = [255, 255, 255, 0];
//         //     }
//         //     controller.render().unwrap();
//         //     // sleep(Duration::from_millis(10));

//         //     let leds = controller.leds_mut(0);
//         //     for led in leds.iter_mut() {
//         //         *led = [0, 0, 0, 0];
//         //     }
//         //     controller.render().unwrap();
//         //     sleep(Duration::from_millis(1000/11));
//         // }
//     }
// }
use axum::{
    extract::{Request, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post, put},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use tokio::{sync::Mutex, task, time::sleep};
use tracing::{debug, Span};

#[tokio::main]
async fn main() {
    // initialize tracing
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .init();
    //console_subscriber::init();

    let state = Arc::new(Mutex::new(LightState {
        on: true,
        bri: 50,
        // hue: 22573,
        // sat: 200,
        xy: [0.0, 0.0],
        effect: LightEffect::None,
    }));

    let local = task::LocalSet::new();

    local.spawn_local({
        let state = Arc::clone(&state);
        async move {
            let mut controller = ControllerBuilder::new()
                .freq(800_000)
                .dma(10)
                .channel(
                    0, // Channel Index
                    ChannelBuilder::new()
                        .pin(10) // GPIO 10 = SPI0 MOSI
                        .count(300) // Number of LEDs
                        .strip_type(StripType::Ws2812)
                        .brightness(255) // default: 255
                        .build(),
                )
                .build()
                .unwrap();

            loop {
                let n = 25500;
                for p in 0..n {
                    let shared_state = state.lock().await;
                    let state = shared_state.clone();
                    drop(shared_state);
                    let c = match state.effect {
                        LightEffect::None => state.rgb(),
                        LightEffect::Colorloop => {
                            let v = if state.on {
                                state.bri as f32 / 255.0
                            } else {
                                0.0
                            };
                            HSV::from_f32(p as f32 / n as f32, 255 as f32 / 255.0, v).to_rgb()
                        }
                    };
                    let c = [
                        (c.b * 255.0) as u8,
                        (c.g * 255.0) as u8,
                        (c.r * 255.0) as u8,
                        0,
                    ];

                    let leds = controller.leds_mut(0);
                    for led in leds.iter_mut() {
                        *led = c;
                    }

                    controller.render().unwrap();
                    sleep(Duration::from_millis(10)).await;
                }
            }
        }
    });

    local.spawn_local(async move {
        // build our application with a route
        let app = Router::new()
            // `GET /` goes to `root`
            .route("/", get(root))
            // `POST /users` goes to `create_user`
            .route("/users", post(create_user))
            .route("/api/{username}/groups", get(get_groups))
            .route("/api/{username}/lights", get(get_all_lights))
            .route(
                "/api/{username}/lights/{id}/state",
                put(set_light_state).get(get_light_state),
            )
            .route(
                "/api/{username}/groups/{id}/action",
                put(set_light_state).get(get_light_state),
            )
            .route("/api/", post(post_create_device))
            .route("/api/{username}", get(get_full_state))
            .with_state(state)
            .layer(tower_http::trace::TraceLayer::new_for_http());

        // run our app with hyper, listening globally on port 3000
        let listener = tokio::net::TcpListener::bind("0.0.0.0:6969").await.unwrap();
        axum::serve(listener, app).await.unwrap();
    });
    local.await;
}

#[derive(Clone, Debug, Serialize)]
struct LightState {
    on: bool,
    bri: u8,
    // hue: u16,
    // sat: u8,
    xy: [f32; 2],
    effect: LightEffect,
}

impl LightState {
    fn hsv(&self) -> HSV {
        HSV::new() // TODO
    }

    fn rgb(&self) -> RGB {
        if !self.on {
            return RGB::new();
        }
        let m = Mat3::from_cols_array(&[
            2.768892, 1.751748, 1.130160, 1.0, 4.5907700, 0.060100, 0.0, 0.056508, 5.594292,
        ])
        .transpose()
        .inverse();
        let x = self.xy[0];
        let y = self.xy[1];
        let z = 1.0 - x - y;
        #[allow(non_snake_case)]
        let Y = self.bri as f32 / u8::MAX as f32;
        // 1 = x + y + z
        // x = X/(X+Y+Z)
        // y = Y/(X+Y+Z)
        // z = Z/(X+Y+Z)
        #[allow(non_snake_case)]
        let X = if y == 0.0 { 0.0 } else { x * Y / y };
        #[allow(non_snake_case)]
        let Z = if y == 0.0 { 0.0 } else { z * Y / y };
        let c = m * Vec3::from_array([X, Y, Z]);
        RGB::from_f32(c.x, c.y, c.z)
    }
}

#[derive(Serialize)]
struct InnerLightStateResponse {
    on: bool,
    bri: u8,
    hue: u16,
    sat: u8,
    effect: LightEffect,
    xy: [f32; 2],
    ct: u16,
    alert: String,
    colormode: String,
    reachable: bool,
}

#[derive(Deserialize)]
struct SetLightState {
    on: Option<bool>,
    bri: Option<u8>,
    hue: Option<u16>,
    xy: Option<[f32; 2]>,
    sat: Option<u8>,
    effect: Option<LightEffect>,
}

#[derive(Serialize)]
struct InnerSetLightStateResponse<T> {
    success: HashMap<String, T>,
}

type SetLightResponse = Vec<Box<dyn erased_serde::Serialize>>;

#[derive(Deserialize, Debug, Clone, Serialize, Copy)]
enum LightEffect {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "colorloop")]
    Colorloop,
}

#[derive(Serialize)]
struct LightStateResponse {
    state: InnerLightStateResponse,
    #[serde(rename = "type")]
    ty: String,
    name: String,
    modelid: String,
    swversion: String,
}

async fn get_light_state(State(state): State<Arc<Mutex<LightState>>>) -> Json<LightStateResponse> {
    let state = state.lock().await;
    let hsv = state.hsv();
    Json(LightStateResponse {
        state: InnerLightStateResponse {
            on: state.on,
            bri: state.bri,
            hue: (hsv.h * u16::MAX as f32) as u16,
            sat: (hsv.s * u8::MAX as f32) as u8,
            effect: state.effect,
            xy: state.xy,
            ct: 0,
            alert: "none".to_string(),
            colormode: "hs".to_string(),
            reachable: true,
        },
        ty: "Extended color light".to_string(),
        name: "Hue Lamp 1".to_string(),
        modelid: "LCT001".to_string(),
        swversion: "65003148".to_string(),
    })
}

async fn set_light_state(
    State(state): State<Arc<Mutex<LightState>>>,
    Json(set_state): Json<SetLightState>,
) -> Json<SetLightResponse> {
    let mut state = state.lock().await;
    let mut response = vec![];
    fn push_response<T: Serialize + 'static>(
        response: &mut SetLightResponse,
        path: &str,
        value: T,
    ) {
        response.push(Box::new(InnerSetLightStateResponse {
            success: {
                let mut m = HashMap::new();
                m.insert(path.to_string(), value);
                m
            },
        }));
    }
    if let Some(on) = set_state.on {
        push_response(&mut response, "/lights/1/state/on", on);
        state.on = on;
    }
    if let Some(bri) = set_state.bri {
        push_response(&mut response, "/lights/1/state/bri", bri);
        state.bri = bri;
    }
    if let Some(hue) = set_state.hue {
        // push_response(&mut response, "/lights/1/state/hue", hue);
        // state.hue = hue;
    }
    if let Some(sat) = set_state.sat {
        // push_response(&mut response, "/lights/1/state/sat", sat);
        // state.sat = sat;
    }
    if let Some(xy) = set_state.xy {
        push_response(&mut response, "/lights/1/state/xy", xy);
        state.xy = xy;
    }
    if let Some(effect) = set_state.effect {
        push_response(&mut response, "/lights/1/state/effect", effect);
        state.effect = effect;
    }
    Json(response)
}

#[derive(Deserialize)]
struct CreateDeviceRequest {
    devicetype: String,
}

async fn post_create_device(Json(payload): Json<CreateDeviceRequest>) -> impl IntoResponse {
    (
        [("content-type", "application/json")],
        include_str!("./post_create_device_sample_response.json"),
    )
}

async fn get_full_state() -> impl IntoResponse {
    (
        [("content-type", "application/json")],
        include_str!("./get_full_state_sample_response.json"),
    )
}

async fn get_groups() -> impl IntoResponse {
    (
        [("content-type", "application/json")],
        include_str!("./get_groups_sample_response.json"),
    )
}

async fn get_all_lights() -> &'static str {
    include_str!("./get_all_lights_sample_response.json")
}

// basic handler that responds with a static string
async fn root() -> &'static str {
    "Hello, World!"
}

async fn create_user(
    // this argument tells axum to parse the request body
    // as JSON into a `CreateUser` type
    Json(payload): Json<CreateUser>,
) -> (StatusCode, Json<User>) {
    // insert your application logic here
    let user = User {
        id: 1337,
        username: payload.username,
    };

    // this will be converted into a JSON response
    // with a status code of `201 Created`
    (StatusCode::CREATED, Json(user))
}

// the input to our `create_user` handler
#[derive(Deserialize)]
struct CreateUser {
    username: String,
}

// the output to our `create_user` handler
#[derive(Serialize)]
struct User {
    id: u64,
    username: String,
}
