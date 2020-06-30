from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .utils.sql_compat import SqliteNumeric

db = SQLAlchemy()
Column, String, Text, DECIMAL, Model, DateTime, Integer, Boolean = \
    db.Column, db.String, db.Text, SqliteNumeric, db.Model, db.DateTime, \
    db.Integer, db.Boolean


class DefaultMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间",
    )
    created_at = Column(
        DateTime, default=datetime.utcnow, comment="创建时间"
    )


class DayKLine(DefaultMixin, Model):
    kline_date = Column(DateTime)
    price_open = Column(DECIMAL(precision="36,18"))
    price_close = Column(DECIMAL(precision="36,18"))
    price_high = Column(DECIMAL(precision="36,18"))
    price_low = Column(DECIMAL(precision="36,18"))
    bottom = Column(Boolean, default=False)
