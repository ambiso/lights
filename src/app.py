import json
import os

from flask import Flask, request, send_from_directory

from src import main

app = Flask(__name__)

@app.route('/')
def home():
    print(os.getcwd())
    return send_from_directory('../static', "index.html")

@app.route('/brightness/<brightness>', methods=['POST'])
def set_brightness(brightness):
    b = float(brightness)
    if 0. < b < 1.:
        main.current_brightness = b
        return json.dumps({"sucess": True, "brightness": b}, separators=(",", ":"))
    else:
        return json.dumps({"sucess": False})

def run():
    app.run(host="0.0.0.0", port=1337)