from apps import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # 테이블명 설정 (users)
    __tablename__ = "users"
    __bind_key__ = "userDB"

    user_id = db.Column(db.String(15), primary_key=True)
    user_password = db.Column(db.String(200), nullable=False)
    user_nickname = db.Column(db.String(80), unique=True, nullable=False)
    user_phone_number = db.Column(db.String(13), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True)

    def get_id(self):
        return self.user_id

    def get_pw(self):
        return self.user_password


class Device(db.Model):
    # 테이블명 설정 (devices)
    __tablename__ = "devices"
    __bind_key__ = "userDB"

    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_serial = db.Column(db.String(16), nullable=False, unique=True)
    device_alias = db.Column(db.String(17), nullable=False)
    user_id = db.Column(db.String(15), nullable=False)

    def get_id(self):
        return self.device_id


class UserInfo(db.Model):
    # 테이블명 설정 (user_info)
    __tablename__ = "user_info"
    __bind_key__ = "resultDB"

    userID = db.Column(db.String(15), primary_key=True)
    video_num = db.Column(db.Integer, primary_key=True)
    re_ID = db.Column(db.String(45), nullable=True)

    def get_userID(self):
        return self.userID


class GameInfo(db.Model):
    # 테이블명 설정 (game_info)
    __tablename__ = "game_info"
    __bind_key__ = "resultDB"

    video_num = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(
        db.String(40), nullable=False
    )  # hazel_20240503_141253_000612.mp4
    userID = db.Column(db.String(15), nullable=False)
    re_ID = db.Column(db.String(45), primary_key=True)
    s_t = db.Column(db.Integer, nullable=False)
    s_s = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

    def get_video_num(self):
        return self.video_num

    def get_re_ID(self):
        return self.re_ID

    def get_fileName(self):
        return self.fileName
