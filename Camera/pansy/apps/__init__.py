from datetime import timedelta
from configs import flask_config
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from sqlalchemy import MetaData

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def register_router(flask_app: Flask):
    # router들을 등록 해주는 곳
    from routers.home import home
    from routers.start_rec_router import start_rec
    from routers.stop_rec_router import stop_rec
    from routers.video_feed_router import video_feed
    from routers.auth import auth

    # 라우팅
    flask_app.register_blueprint(home)
    flask_app.register_blueprint(start_rec)
    flask_app.register_blueprint(stop_rec)
    flask_app.register_blueprint(video_feed)
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
    db.init_app(app)
    register_router(app)

    # flask-login 적용
    login_manager = LoginManager()
    login_manager.login_view = "sign-in"
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)  # primary_key

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("auth.sign_in"))

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=120)

    return app


def get_flask_env():
    # 환경변수에 따라 config나누기
    if flask_config.Config.ENV == "prod":
        return "configs.flask_config.prodConfig"
    elif flask_config.Config.ENV == "dev":
        return "configs.flask_config.devConfig"
