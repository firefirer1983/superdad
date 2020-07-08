import os

from dotenv import load_dotenv
from flask import Flask

from .handler import register_logging, register_errors, register_blueprints, \
    register_commands, register_extensions, register_jinja_filters, \
    register_tasks, register_token_bucket
from .settings import config
DOT_ENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".flaskenv")
load_dotenv(DOT_ENV, override=True)


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config[os.environ["FLASK_ENV"]])
    
    register_jinja_filters(app)
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_tasks(app)
    register_token_bucket(app)
    register_commands(app)
    register_errors(app)
    return app



