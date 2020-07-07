from flask_marshmallow import Marshmallow

from .model import DayKline

ma = Marshmallow()


class DateRangeSchema(ma.Schema):
    pass


class DayHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DayKline
        include_relationships = True
        load_instance = True


daily_history_schema = DayHistorySchema()
