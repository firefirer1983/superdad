from flask import Blueprint, render_template, request, jsonify

from .plates import china_plates
from ..gateway import gateway
from ..model import Favourite

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
@dashboard_bp.route("/favourites", methods=["GET"])
def favourites():
    ret = Favourite.list_stock()
    favs = sorted([fav.market_code for fav in ret])
    stocks = []
    if favs:
        stocks = gateway.get_snap_shot(favs)
    return render_template("dashboard.html",
                           titles=["股票代码", "更新时间", "最新价格"],
                           favs=stocks)


@dashboard_bp.route("/plates", methods=["GET"])
def plates():
    return render_template("plates.html", plates=china_plates)


@dashboard_bp.route("/markets", methods=["GET"])
def markets():
    code = request.args.get("code")
    stocks = gateway.list_stock_by_plate(code)
    favourite_list = Favourite.list_stock()
    return render_template(
        "markets.html",
        cols=stocks.keys(),
        rows=stocks,
        favs=sorted([fav.market_code for fav in favourite_list]))


@dashboard_bp.route("/favourites/add", methods=["POST"])
def add_to_favourite():
    code = request.get_json().get("code")
    Favourite(market_code=code).save()
    return jsonify(res="ok")


@dashboard_bp.route("/favourites/remove", methods=["POST"])
def remove_favourite(code):
    market, code = code.split(".")
    Favourite.query.filter_by(market=market).filter_by(code=code).one()
    return jsonify(res="ok")
