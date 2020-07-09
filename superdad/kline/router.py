import datetime

from flask import Blueprint, request, render_template
from ..i18n import kline_trans
from ..model import DayKline
from ..utils.strs import DAY_FORMAT, str_to_datetime

kline_bp = Blueprint("kline", __name__)


def first_day_of_year(year):
    return datetime.datetime.strptime("%s-01-01" % year, DAY_FORMAT)


@kline_bp.route("/kline/<market_code>", methods=["GET"])
def get_history(market_code):
    query_param = request.get_json()
    day_range = query_param.get("day_range", None) if query_param else None
    if day_range:
        begin, end = str_to_datetime(
            day_range["from_date"]), str_to_datetime(day_range["to_date"])
    else:
        end, begin = datetime.date.today(), first_day_of_year(
            datetime.date.today().year)
    titles, rows = DayKline.list_history(market_code=market_code, begin=begin,
                                         end=end)
    rows = [r.to_dict() for r in rows]
    return render_template("kline.html", rows=rows, titles=titles,
                           hidden=["id", "updated_at", "created_at"],
                           trans=kline_trans)
