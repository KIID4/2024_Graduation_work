from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_login import login_required, current_user
from utils.paint_graph import get_all_basketball_play_shooting_mean_graph
from models import GameInfo, UserInfo
import matplotlib as plt

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def show_dashboard():
    games = GameInfo.query.filter_by(userID=current_user.get_id()).all()

    result_games = []
    first = None
    for game in games:
        if first == game.get_fileName():
            continue
        else:
            first = game.get_fileName()
            result_games.append(game)

    return render_template(
        "dashboard.html",
        games=result_games,
        # , first_card_graph=get_all_basketball_play_shooting_mean_graph()
    )


@dashboard.route("/dashboard_detail", methods=["GET", "POST"])
@login_required
def show_detail():
    video_num = request.form.get("video_num")
    fileName = request.form.get("fileName")
    selected_games = GameInfo.query.filter_by(
        userID=current_user.get_id(), video_num=video_num, fileName=fileName
    ).all()

    return render_template("dashboard_detail.html", games=selected_games)
