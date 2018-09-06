from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    app.static_folder = 'static'
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
