import datetime

from flask import Blueprint, request, render_template

from ..gateway import gateway
from ..utils.strs import DAY_FORMAT, str_to_datetime
from ..model import DayKline

kline_bp = Blueprint("kline", __name__)


def first_day_of_year(year):
    return datetime.datetime.strptime("%s-01-01" % year, DAY_FORMAT)


@kline_bp.route("/kline/<market_code>", methods=["GET"])
def get_history(market_code):
    query_param = request.get_json()
    day_range = query_param.get("day_range", None) if query_param else None
    if day_range:
        from_date, to_date = str_to_datetime(
            day_range["from_date"]), str_to_datetime(day_range["to_date"])
    else:
        to_date, from_date = datetime.date.today(), first_day_of_year(
            datetime.date.today().year)
    return render_template("kline.html", data=[])
