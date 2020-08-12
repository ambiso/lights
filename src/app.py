import json
import os
import sys

from flask import Flask, request, render_template

from src import main

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("index.html", animation=main.curr_animations, brightness=main.curr_brightness)

@app.route('/brightness/<brightness>', methods=['POST'])
def set_brightness(brightness):
	b = int(brightness)
	if 0 <= b <= 255:
		main.curr_brightness = b
		return json.dumps({"sucess": True, "brightness": b})
	else:
		return json.dumps({"sucess": False})


@app.route('/animation/<animation>', methods=['POST'])
def toggle_animation(animation):
	if animation not in animations:
		return json.dumps({"sucess": False})
	anim_fn = animations[animation]
	if anim_fn in main.curr_animations:
		main.curr_animations.remove(anim_fn)
	else:
		main.curr_animations.append(animations[animation])
	return json.dumps({"sucess": True, "animation": [fn.__name__ for fn in main.curr_animations]})

def run():
	app.run(host="0.0.0.0", port=1337)