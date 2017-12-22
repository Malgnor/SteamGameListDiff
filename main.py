import os
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/key')
def show_key():
    return 'Steam web api key: ' + os.getenv('STEAM_WEB_API_KEY', 'NO KEY :(')
