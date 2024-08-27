import base64
from io import BytesIO
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from utils.gen_qrcode import generate_qrcode
from utils.validated import is_valid_device_alias
from models import db, Device

cam_control = Blueprint("cam_control", __name__)


@cam_control.route("/device_registration", methods=["GET", "POST"])
@login_required
def register_device():
    if request.method == "POST":
        # 네트워크 이름(ssid)
        network_ssid = request.form.get("network_ssid").strip()
        session["network_ssid"] = network_ssid

        # 네트워크 암호화방식
        network_security = request.form.get("network_security").strip()
        session["network_security"] = network_security

        # 네트워크 비밀번호(password)
        network_pw = request.form.get("network_pw").strip()
        session["network_pw"] = network_pw

        # user의 아이디
        user_id = current_user.get_id().strip()

        # 기기 별칭(사용자 소유 기기 내 unique)
        device_alias = request.form.get("device_alias").strip()
        session["device_alias"] = device_alias

        # 유효성 검사
        qrcode_data = []
        qrcode_info = {}
        qrcode_info["Network_SSID"] = network_ssid
        qrcode_data.append(network_ssid)
        qrcode_info["Security"] = network_security
        qrcode_data.append(network_security)
        qrcode_info["Network_PW"] = network_pw
        qrcode_data.append(network_pw)
        qrcode_info["Owner"] = user_id
        qrcode_data.append(user_id)

        device = Device.query.filter_by(
            user_id=user_id, device_alias=device_alias
        ).first()
        if 1 <= len(network_pw) < 8:
            flash(
                "네트워크 비밀번호는 8자 이상 입력바랍니다.",
                category="error",
            )
        elif device:
            flash(
                "보유 기기와 기기별칭이 중복됩니다.",
                category="error",
            )
        elif not is_valid_device_alias(device_alias, 2, 17):
            flash(
                "기기별칭은 영문자, 숫자, '-', '_'만 사용가능하며, 2~17자 내로 입력바랍니다.",
                category="error",
            )
        else:
            qrcode_info["Device_Alias"] = device_alias
            qrcode_data.append(device_alias)
            # flash("정상적으로 QR코드가 생성되었습니다.", category="success")

            session.pop("network_ssid", None)
            session.pop("network_security", None)
            session.pop("network_pw", None)
            session.pop("device_alias", None)

            return render_template(
                "qrcode.html",
                qrcode_image=generate_qrcode(qrcode_data),
                qrcode_info=qrcode_info,
            )

    return render_template("device_registration.html")


@cam_control.route("/devices")
@login_required
def show_devices():
    # 보유 기기 목록을 세션에 저장
    own_devices = Device.query.filter_by(user_id=current_user.get_id()).all()

    return render_template("devices.html", devices=own_devices)
