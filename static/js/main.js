async function change_brightness() {
	let brightness = document.querySelector(".input-brightness").value;
	console.log(`brightness: ${brightness}`);
	let res = await fetch(`/brightness/${brightness / 100}`, { method: 'POST' });
	console.log(res.json());
}

async function change_animation() {
	let e = document.getElementById("animation");
	let animation = e.options[e.selectedIndex].value;
	console.log(`animation: ${animation}`);
	let res = await fetch(`/animation/${animation}`, { method: 'POST' })
	console.log(res.json());
}