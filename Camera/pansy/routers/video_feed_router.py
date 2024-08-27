from flask import Blueprint, Response, g, render_template, send_file
from flask_login import login_required
from utils.camera import Camera

video_feed = Blueprint("video_feed", __name__)


@video_feed.route("/streaming", methods=["GET"])
@login_required
def streaming():
    print("\n\n스트리밍!\n\n")
    """인증
    if not check_auth():
        return jsonify({'message': 'Unauthorized'}), 401
    """

    cam3 = Camera.instance()

    if cam3.is_recording == False:  # 녹화는 끝났지만, frame 쓰는 중임
        # Accepted (클라이언트에 우선 요청을 잘 받았다고 알리고, 즉시 돌아와서 남은 동작 수행)
        return "", 202

    return Response(
        response=cam3.gen_frame(),
        mimetype="multipart/x-mixed-replace; boundary=FRAME",
    )
