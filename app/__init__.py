from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('errors/401.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app
