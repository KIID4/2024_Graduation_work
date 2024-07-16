from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_login import login_required, current_user


views = Blueprint("views", __name__)


@views.route("/")
def index():
    return redirect(url_for("auth.sign_in"))
