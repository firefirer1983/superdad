from flask import Blueprint, render_template

from ..gateway import gateway
from ..model import Favourites

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder='static'
)


@dashboard_bp.route("/", methods=["GET"])
@dashboard_bp.route("/favourites", methods=["GET"])
def favourites():
    ret = Favourites.list_stock()
    return render_template('dashboard.html', favourte_list=ret)


@dashboard_bp.route("/markets", methods=["GET"])
def markets():
    sz = gateway.get_sz_basic_info()
    sh = gateway.get_sh_basic_info()
    return render_template("market.html")
