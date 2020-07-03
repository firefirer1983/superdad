from flask_marshmallow import Marshmallow

from .model import DailyHistory

ma = Marshmallow()


class DateRangeSchema(ma.Schema):
    pass


class DayHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyHistory
        include_relationships = True
        load_instance = True


daily_history_schema = DayHistorySchema()
