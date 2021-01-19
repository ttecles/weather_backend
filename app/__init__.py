from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.helpers import BaseQueryJSON
from config import config

db = SQLAlchemy(query_class=BaseQueryJSON)


def _register_blueprints(app: Flask):
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from app.errors import bp_errors
    app.register_blueprint(bp_errors)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    _register_blueprints(app)

    return app
