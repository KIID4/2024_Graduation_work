import os
from werkzeug.security import check_password_hash
from dotenv import load_dotenv


def is_valid_owner(given_user, given_pass):
    load_dotenv()
    return given_user == os.environ.get("DEVICE_OWNER") and check_password_hash(
        os.environ.get("SECRET"), given_pass
    )



