from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from models import db
from flask_login import login_user, login_required, logout_user, current_user
from utils.validated import (
    is_valid_email,
    is_valid_id,
    is_valid_password,
    is_valid_nickname,
    is_valid_phone_number,
)

auth = Blueprint("auth", __name__)


@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.show_dashboard"))

    # login
    if request.method == "POST":
        user_id = request.form.get("id")
        session["sign-in-id"] = user_id
        user_password1 = request.form.get("password1")

        # search User in database & compare password
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            if check_password_hash(user.user_password, user_password1):
                if session.pop(user_id, None):
                    flash("동시접속을 차단합니다.", category="error")
                    return redirect(url_for("auth.logout"))
                else:
                    # login_user(user, remember=True)  # 내용 기억하기
                    login_user(user)
                    flash("로그인 성공", category="success")
                    print("로그인 성공!")
                    return redirect(url_for("dashboard.show_dashboard"))
            else:
                flash("아이디 혹은 비밀번호가 틀렸습니다.", category="error")
        else:
            flash("해당 아이디 정보가 없습니다.", category="error")
    return render_template("sign-in.html")


@auth.route("/logout")
@login_required
def logout():
    session.pop(current_user.get_id(), None)
    logout_user()
    return redirect(url_for("views.index"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # form - input의 name 속성을 기준으로 가져오기
        user_id = request.form.get("id")
        session["sign-up-id"] = user_id
        user_password1 = request.form.get("password1")
        session["sign-up-password1"] = user_password1
        user_password2 = request.form.get("password2")
        session["sign-up-password2"] = user_password2
        user_nickname = request.form.get("nickname")
        session["sign-up-nickname"] = user_nickname
        user_phone_number = request.form.get("phone-number")
        session["sign-up-phoneNumber"] = user_phone_number
        user_email = request.form.get("email")
        session["sign-up-email"] = user_email
        sign_up_agree = request.form.get("agree")
        session["sign-up-agree"] = sign_up_agree

        # 유효성 검사
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            flash("이미 가입된 아이디입니다.", category="error")
            session.pop("sign-up-id", None)
        elif not is_valid_id(user_id, 4, 15):
            flash(
                "아이디는 숫자,영문자,'-','_'만 가능하며, 4~15자 내로 입력바랍니다.",
                category="error",
            )
        elif not is_valid_password(user_password1, 4, 200):
            flash("비밀번호는 공백 문자 제외 4자 이상 입력바랍니다.", category="error")
        elif user_password1 != user_password2:
            flash("비밀번호 재입력이 불일치합니다.", category="error")
            session.pop("sign-up-password2", None)
        elif not is_valid_nickname(user_nickname, 2, 80):
            flash(
                "닉네임은 숫자,영문자,'-','_'만 가능하며, 2자 이상 입력바랍니다.",
                category="error",
            )
        elif not is_valid_phone_number(user_phone_number):
            flash("전화번호는 '-' 를 제외하고 11자입니다.", category="error")
        elif not is_valid_email(user_email):
            flash("올바른 이메일 형식으로 입력바랍니다.", category="error")
        elif not sign_up_agree:
            flash("개인정보 수집에 동의해 주시기 바랍니다.", category="error")

        else:
            # Create User > DB
            new_user = User(
                user_id=user_id,
                user_password=generate_password_hash(
                    user_password1, method="pbkdf2:sha256"
                ),
                user_nickname=user_nickname,
                user_phone_number=f"{user_phone_number[:3]}-{user_phone_number[3:7]}-{user_phone_number[7:]}",
                user_email=user_email,
            )
            db.session.add(new_user)
            db.session.commit()

            session.pop("sign-up-id", None)
            session.pop("sign-up-password1", None)
            session.pop("sign-up-password2", None)
            session.pop("sign-up-nickname", None)
            session.pop("sign-up-phoneNumber", None)
            session.pop("sign-up-email", None)
            session.pop("sign-up-agree", None)
            flash("회원가입이 완료되었습니다.", category="success")  # Create User -> DB
            return redirect(url_for("views.index"))

    return render_template("sign-up.html")
