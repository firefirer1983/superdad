import datetime
import logging
from functools import wraps
from urllib.parse import quote_plus

import click
from flask import jsonify
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from .tasks import kliner, trender
from .dashboard import dashboard_bp
from .exc import JsonErrorResponse
from .gateway import gateway
from .kline import kline_bp
from .limiter import limit
from .model import db
from .schema import ma


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


scheduler = APScheduler()


def next_tick(sec):
    return datetime.datetime.now() + datetime.timedelta(seconds=sec)


def register_tasks(flsk):
    scheduler.init_app(flsk)
    cron_task(kliner.update, flsk, scheduler, "update-kline-task", 10)
    # cron_task(limit.refill, flsk, scheduler, "refill-bucket-task", 60)
    cron_task(trender.process, flsk, scheduler, "refill-bucket-task", 10)
    scheduler.start()


def register_token_bucket(flsk):
    gateway.init_app(flsk)
    limit.init_app(flsk)


def cron_task(f, app, sched, task_id="", interval=60):
    @wraps(f)
    def _f():
        with app.app_context():
            ret = f()
        sched.add_job(id=task_id, func=_f, next_run_time=next_tick(interval))
        return ret

    sched.add_job(id=task_id, func=_f, next_run_time=next_tick(interval))
    return _f


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


def register_jinja_filters(fsk):
    fsk.jinja_env.filters["quote_plus"] = lambda x: quote_plus(x)


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
