from dotenv import load_dotenv
from flask import Blueprint, redirect, render_template, request, url_for
from utils.auth import is_valid_owner

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def sign_in():
    # login
    if request.method == "POST":
        load_dotenv()
        user_id = request.form.get("id")
        user_pw = request.form.get("password")
        if is_valid_owner(user_id, user_pw):
            print("로그인 성공!")
            return redirect(url_for("home.go_home"))
        else:
            return render_template("sign-in.html", login_failed=True)

    return render_template("sign-in.html")
