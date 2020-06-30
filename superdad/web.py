import os

from dotenv import load_dotenv
from flask import Flask

from .handler import register_logging, register_errors, register_blueprints, \
    register_commands, register_extensions
from .settings import config

DOT_ENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".flaskenv")
load_dotenv(DOT_ENV, override=True)

app = Flask(__name__)
app.config.from_object(config[os.environ["FLASK_ENV"]])

register_logging(app)
register_extensions(app)
register_blueprints(app)
register_commands(app)
register_errors(app)
