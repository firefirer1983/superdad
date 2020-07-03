from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .utils.sql_compat import SqliteNumeric
from .utils.strs import datetime_to_day_str, day_str_to_datetime

db = SQLAlchemy()
Column, String, Text, DECIMAL, Model, DateTime, Integer, Boolean, Index = \
    db.Column, db.String, db.Text, SqliteNumeric, db.Model, db.DateTime, \
    db.Integer, db.Boolean, db.Index


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


class DailyHistory(DefaultMixin, Model):
    time_key = Column(DateTime)
    market = Column(String(8))
    code = Column(String(16))
    open = Column(DECIMAL(precision="36,18"))
    close = Column(DECIMAL(precision="36,18"))
    high = Column(DECIMAL(precision="36,18"))
    low = Column(DECIMAL(precision="36,18"))
    pe_ratio = Column(DECIMAL(precision="36,18"))
    turnover_rate = Column(DECIMAL(precision="36,18"))
    volume = Column(Integer)
    turnover = Column(DECIMAL(precision="36,18"))
    change_rate = Column(DECIMAL(precision="36,18"))
    last_close = Column(DECIMAL(precision="36,18"))
    
    @property
    def day(self):
        return day_str_to_datetime(datetime_to_day_str(self.date))


class Favourites(DefaultMixin, Model):
    market = Column(String(8))
    code = Column(String(16))
    
    def __init__(self, market_code):
        self.market, self.code = market_code.split(".")
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def list_stock(cls):
        return cls.query.all() or []


Index('market_code', Favourites.market, Favourites.code, unique=True)
