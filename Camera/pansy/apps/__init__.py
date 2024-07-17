from flask import Flask
from configs import flask_config


def register_router(flask_app: Flask):
    # router들을 등록 해주는 곳
    from routers.home import home
    from routers.start_rec_router import start_rec
    from routers.stop_rec_router import stop_rec
    from routers.video_feed_router import video_feed
    from temp.py.connect_network import connect_network
    from routers.auth import auth

    # 라우팅
    flask_app.register_blueprint(home)
    flask_app.register_blueprint(start_rec)
    flask_app.register_blueprint(stop_rec)
    flask_app.register_blueprint(video_feed)
    flask_app.register_blueprint(connect_network)
    flask_app.register_blueprint(auth)

    # app의 request/response들과 매번 함께 실행할 함수 정의
    """
    @flask_app.before_request
    def before_my_request():
        print("before my request")

    @flask_app.after_request
    def after_my_request(res):
        print("after my request", res.status_code)
        return res
    """


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(get_flask_env())
    register_router(app)
    return app


def get_flask_env():
    # 환경변수에 따라 config나누기
    if flask_config.Config.ENV == "prod":
        return "config.flask_config.prodConfig"
    elif flask_config.Config.ENV == "dev":
        return "config.flask_config.devConfig"
