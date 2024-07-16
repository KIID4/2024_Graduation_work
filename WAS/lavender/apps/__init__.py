from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from configs import flask_config
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
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
    from routers.auth import auth
    from routers.views import views
    from routers.cam_control import cam_control
    from routers.dashboard import dashboard

    flask_app.register_blueprint(views)
    flask_app.register_blueprint(auth)
    flask_app.register_blueprint(cam_control)
    flask_app.register_blueprint(dashboard)


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
        return redirect(url_for("views.index"))

    migrate = Migrate(app, db, render_as_batch=True)

    return app


def get_flask_env():
    # 환경변수에 따라 config나누기
    if flask_config.Config.ENV == "prod":
        return "configs.flask_config.prodConfig"
    elif flask_config.Config.ENV == "dev":
        return "configs.flask_config.devConfig"
