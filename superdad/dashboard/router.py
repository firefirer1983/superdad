from flask import Blueprint, render_template, request

from ..gateway import gateway
from ..model import Favourites
from .plates import china_plates


dashboard_bp = Blueprint(
    "dashboard", __name__, template_folder="templates", static_folder="static"
)


@dashboard_bp.route("/", methods=["GET"])
@dashboard_bp.route("/favourites", methods=["GET"])
def favourites():
    ret = Favourites.list_stock()
    return render_template("dashboard.html", favourte_list=ret)


@dashboard_bp.route("/plates", methods=["GET"])
def plates():
    return render_template("plates.html", plates=china_plates)


@dashboard_bp.route("/markets", methods=["GET"])
def markets():
    code = request.args.get("code")
    stocks = gateway.list_stock_by_plate(code)
    return render_template("markets.html", cols=stocks.keys(), rows=stocks)
