import logging
import click
from .model import db
from .validator import ma
from .exc import JsonErrorResponse
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_bootstrap import Bootstrap
from flask import jsonify
from .kline import kline_bp
from .dashboard import dashboard_bp


def register_logging(flsk):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    flsk.logger.setLevel(flsk.config["LOG_LEVEL"])
    flsk.logger.addHandler(console)


def register_blueprints(flsk):
    flsk.register_blueprint(kline_bp)
    flsk.register_blueprint(dashboard_bp)


def register_extensions(flsk):
    Bootstrap(flsk)
    db.init_app(flsk)
    ma.init_app(flsk)


def register_errors(flsk):
    # marshmallow validate error
    flsk.register_error_handler(ValidationError, handle_validation_error)
    # customize json error
    flsk.register_error_handler(JsonErrorResponse, handle_json_error)
    # sqlalchemy error
    flsk.register_error_handler(SQLAlchemyError, handle_db_error)


def register_commands(flsk):
    @flsk.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop.")
    def init_db(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                "This will delete the database, do you want to continue?",
                abort=True,
            )
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")


def handle_json_error(e):
    rsp = jsonify(e.to_dict())
    rsp.status_code = e.status_code
    return rsp


def handle_db_error(e):
    print(str(e))
    rsp = jsonify({"message": "Database Error %s" % str(e)})
    rsp.status_code = 500
    return rsp


def handle_validation_error(e):
    rsp = jsonify({"message": "Input Parameter Validate Error %s" % str(e)})
    rsp.status_code = 400
    return rsp
