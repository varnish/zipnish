from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)

    app.config_from_object(config[config_name])

    return app
