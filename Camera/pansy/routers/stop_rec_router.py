from datetime import datetime
import threading
from flask import Blueprint, redirect, url_for
from flask_login import login_required
from utils.camera import Camera

stop_rec = Blueprint("stop_rec", __name__)


@stop_rec.route("/stop_rec", methods=["GET", "POST"])
@login_required
def stop_recording():
    print("\n\n녹화 중지!\n\n")
    cam2 = Camera.instance()
    if cam2.is_recording == True:
        cam2.stop_rec_time = datetime.now()
        cam2.is_recording = False
        threading.Thread(target=cam2.stop_video_writer).start()

    return redirect(url_for("home.go_home"))
