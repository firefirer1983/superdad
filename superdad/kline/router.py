import datetime

from flask import Blueprint, request

from ..gateway import gateway
from ..utils.strs import DAY_FORMAT, datetime_to_day_str

kline_bp = Blueprint(
    "kline",
    __name__,
    template_folder="templates",
    static_folder="static"
)


def first_day_of_year(year):
    return datetime.datetime.strptime("%s-01-01" % year, DAY_FORMAT)


@kline_bp.route("/kline/<market>/<code>", methods=["GET"])
def get_history(market, code):
    query_param = request.get_json()
    day_range = query_param.get("day_range", None) if query_param else None
    if day_range:
        from_date, to_date = day_range["from_date"], day_range["to_date"]
    else:
        to_date = datetime.date.today()
        from_date = first_day_of_year(to_date.year)
    from_date, to_date = datetime_to_day_str(from_date), datetime_to_day_str(to_date)
    print(
        gateway.get_kline_by_days("%s.%s" % (market, code), from_date=from_date,
                                  to_date=to_date))
    return "hello"
