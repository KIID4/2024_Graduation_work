from datetime import datetime
import threading
from flask import Blueprint, redirect, url_for
from flask_login import login_required
from utils.camera import Camera

start_rec = Blueprint("start_rec", __name__)


@start_rec.route("/start_rec", methods=["GET", "POST"])
@login_required
def start_recording():
    print("\n\n녹화 시작!\n\n")
    cam1 = Camera.instance()
    if cam1.is_recording == None:
        cam1.start_rec_time = datetime.now()
        cam1.is_recording = True
        cam1.start_video_writer()
        cam1.record_thread.start()

    return redirect(url_for("home.go_home"))
