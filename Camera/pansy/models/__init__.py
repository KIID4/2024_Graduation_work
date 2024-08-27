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

    def get_serial(self):
        return self.device_serial
