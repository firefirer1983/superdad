from flask import Blueprint, render_template

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder='static'
)


@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    return render_template('dashboard.html', name="xy")
