import os
import logging

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "secret string")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = os.getenv("SQLALCHEMY_RECORD_QUERIES", True)
    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(BaseConfig):
    VERSION = "1.0"
    LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "DEBUG"))
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/dev.db3" % BASEDIR
    WTF_CSRF_ENABLED = False
    EXPLAIN_TEMPLATE_LOADING = True


class TestingConfig(BaseConfig):
    VERSION = "1.0"
    LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "DEBUG"))
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(BaseConfig):
    VERSION = "1.0"
    LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
    SQLALCHEMY_POOL_SIZE = int(os.getenv("POOL_SIZE", 0)) or None
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", 0)) or None
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/prod.db3" % BASEDIR


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
