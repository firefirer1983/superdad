import datetime

from flask import Blueprint, request

from ..gateway import gateway
from ..utils.strs import DAY_FORMAT, str_to_datetime

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
        from_date, to_date = str_to_datetime(
            day_range["from_date"]), str_to_datetime(day_range["to_date"])
    else:
        to_date, from_date = datetime.date.today(), first_day_of_year(
            datetime.date.today().year)
    for month, data in gateway.get_kline_by_month("%s.%s" % (market, code),
                                                  from_date=from_date,
                                                  to_date=to_date):
        print("%u: %r" % (month, data))
    return "hello"
