from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, func

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


class DayKline(DefaultMixin, Model):
    time_key = Column(DateTime)
    market_code = Column(String(32))
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
    
    @classmethod
    def list_history(cls, reverse=True):
        key = cls.time_key
        if not reverse:
            key = asc(cls.time_key)
        
        return cls.query.order_by(key).all() or []
    
    @classmethod
    def latest(cls):
        return db.session.query(func.max(cls.time_key)).one()


class DayAnalyze(DefaultMixin, Model):
    time_key = Column(DateTime)
    market_code = Column(String(32))
    bottom = Column(Boolean, default=False)


class Favourite(DefaultMixin, Model):
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
    
    @property
    def market_code(self):
        return ".".join([self.market, self.code])


Index('market_code', Favourite.market, Favourite.code, unique=True)
Index('day_kline_key', DayKline.market_code, DayKline.time_key, unique=True)
Index('day_analyze_key', DayAnalyze.market_code, DayAnalyze.time_key,
      unique=True)
