from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    moment.init_app(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
