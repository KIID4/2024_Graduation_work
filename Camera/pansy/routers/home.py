from flask import Blueprint, render_template, abort, request, redirect, url_for, session
from jinja2 import TemplateNotFound
from utils.camera import Camera
import os

home = Blueprint("home", __name__)


@home.route("/home", methods=["GET", "POST"])
def go_home():
    print("\n\n홈!\n\n")

    try:
        cam = Camera.instance()

        return render_template(
            "index.html",
            user_name=cam.user_name,
            start_rec_time=cam.start_rec_time,
            duration=cam.duration,
            file_name=cam.file_name,
            is_recording=cam.is_recording,
            # writing_status=cam.get_writing_status(),
        )
    except TemplateNotFound:
        abort(404)
