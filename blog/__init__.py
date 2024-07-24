from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ae13200456753159Ae*'

    from .routes import routes

    app.register_blueprint(routes, url_prefix="/")

    return app 