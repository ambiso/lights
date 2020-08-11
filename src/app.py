import json
import os
import sys

from flask import Flask, request, render_template

from src import main

app = Flask(__name__)

@app.route('/')
def home():
    print(os.getcwd(), file=sys.stderr)
    return render_template("index.html", animation=main.curr_animation, brightness=main.curr_brightness)

@app.route('/brightness/<brightness>', methods=['POST'])
def set_brightness(brightness):
    b = float(brightness)
    if 0. < b < 1.:
        main.curr_brightness = b
        return json.dumps({"sucess": True, "brightness": b}, separators=(",", ":"))
    else:
        return json.dumps({"sucess": False})


@app.route('/animation/<animation>', methods=['POST'])
def set_animation(animation):
    main.curr_animation = animation
    return json.dumps({"sucess": True, "animation": animation}, separators=(",", ":"))

def run():
    app.run(host="0.0.0.0", port=1337)