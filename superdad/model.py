import pdb
from datetime import datetime
from typing import List, Tuple

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, func, and_

from .utils.sql_compat import SqliteNumeric
from .utils.strs import datetime_to_day_str, day_str_to_datetime

db = SQLAlchemy()

Column, String, Text, DECIMAL, Model, DateTime, Integer, Boolean, Index = (
    db.Column,
    db.String,
    db.Text,
    SqliteNumeric,
    db.Model,
    db.DateTime,
    db.Integer,
    db.Boolean,
    db.Index,
)


def columns_of(cls):
    return [col.name for col in cls.__table__.columns]


class DefaultMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间",
    )
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d


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
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @property
    def day(self):
        return day_str_to_datetime(datetime_to_day_str(self.date))
    
    @classmethod
    def list_history(cls, market_code, reverse=True, begin=None, end=None) -> \
        Tuple[List[str], List["DayKline"]]:
        key = cls.time_key
        if not reverse:
            key = asc(cls.time_key)

        criterions = [cls.market_code == market_code]
        if begin:
            criterions.append(cls.time_key >= begin)
        if end:
            criterions.append(cls.time_key < end)
        ret = cls.query.filter(*criterions).order_by(key).all()
        return columns_of(cls), ret or []
    
    @classmethod
    def last_time_key(cls, market_code):
        return (
            db.session.query(func.max(cls.time_key))
                .filter_by(market_code=market_code)
                .scalar()
        )
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class DayTrend(DefaultMixin, Model):
    time_key = Column(DateTime)
    market_code = Column(String(32))
    phase_low = Column(Boolean, default=None)
    price_up = Column(DECIMAL(precision="36,18"), nullable=False)
    volume_up = Column(DECIMAL(precision="36,18"), nullable=False)
    
    @classmethod
    def list_trends(cls, market_code, reverse=True):
        key = cls.time_key
        if not reverse:
            key = asc(cls.time_key)
        return (
            cls.query.filter_by(market_code=market_code).order_by(key).all()
            or []
        )
    
    @classmethod
    def last_time_key(cls, market_code):
        return (
            db.session.query(func.max(cls.time_key))
                .filter_by(market_code=market_code)
                .scalar()
        )
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Favourite(DefaultMixin, Model):
    market = Column(String(8))
    code = Column(String(16))
    
    def __init__(self, market_code):
        self.market, self.code = market_code.split(".")
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def list_stock(cls) -> List["Favourite"]:
        return cls.query.all() or []
    
    @property
    def market_code(self):
        return ".".join([self.market, self.code])


Index("market_code", Favourite.market, Favourite.code, unique=True)
Index("day_kline_key", DayKline.market_code, DayKline.time_key, unique=True)
Index("day_analyze_key", DayTrend.market_code, DayTrend.time_key, unique=True)
