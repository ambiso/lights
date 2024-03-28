use std::{thread::sleep, time::Duration};

use bracket_color::prelude::HSV;
use rs_ws281x::{ChannelBuilder, ControllerBuilder, StripType};

fn main() -> ! {
    // Construct a single channel controller. Note that the
    // Controller is initialized by default and is cleaned up on drop

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
            let c = HSV::from_f32(p as f32 / n as f32, 1.0, 1.0).to_rgb();
            let b = 1.0/(c.b + c.g + c.r);
            let c = [
                (c.b * 255.0 * b) as u8,
                (c.g * 255.0 * b) as u8,
                (c.r * 255.0 * b) as u8,
                0,
            ];

            let leds = controller.leds_mut(0);
            for led in leds.iter_mut() {
                *led = c;
            }

            controller.render().unwrap();
            sleep(Duration::from_millis(10));
        }


        // for p in 0..255 {

        //     let leds = controller.leds_mut(0);
        //     for led in leds.iter_mut() {
        //         *led = [255, 255, 255, 0];
        //     }
        //     controller.render().unwrap();
        //     // sleep(Duration::from_millis(10));

        //     let leds = controller.leds_mut(0);
        //     for led in leds.iter_mut() {
        //         *led = [0, 0, 0, 0];
        //     }
        //     controller.render().unwrap();
        //     sleep(Duration::from_millis(1000/11));
        // }
    }
}
