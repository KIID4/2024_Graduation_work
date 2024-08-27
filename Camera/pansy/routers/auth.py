from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from models import db
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
import os

auth = Blueprint("auth", __name__)


@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for("home.go_home"))

    # login
    if request.method == "POST":
        # load_dotenv()

        user_id = request.form.get("id")
        user_pw = request.form.get("password")

        user = User.query.filter_by(user_id=user_id).first()
        if (user_id == os.environ.get("DEVICE_OWNER")) and check_password_hash(
            user.user_password, user_pw
        ):
            login_user(user)
            print("로그인 성공!")
            return redirect(url_for("home.go_home"))
        else:
            return render_template("sign-in.html", login_failed=True)

    return render_template("sign-in.html")


# --------------------------------------------------------------------------
@auth.route("/logout")
@login_required
def logout():
    session.pop(current_user.get_id(), None)
    logout_user()
    return redirect(url_for("auth.sign_in"))
