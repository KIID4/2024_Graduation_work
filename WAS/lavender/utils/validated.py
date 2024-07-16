import re


def is_valid_id(user_id, min_size, max_size):
    VALID_ID_REGEX = r"^[a-zA-Z0-9_-]{" + f"{min_size},{max_size}" + "}$"
    if not re.fullmatch(VALID_ID_REGEX, user_id):
        return False
    return True


def is_valid_password(user_password, min_size, max_size):
    VALID_PW_REGEX = (
        r"^[a-zA-Z0-9!@#$%^&*\(\)\_\-\=\+]{" + f"{min_size},{max_size}" + "}$"
    )
    if not re.fullmatch(VALID_PW_REGEX, user_password):
        return False
    return True


def is_valid_nickname(user_nickname, min_size, max_size):
    VALID_NICKNAME_REGEX = r"^[a-zA-Z0-9_-]{" + f"{min_size},{max_size}" + "}$"
    if not re.fullmatch(VALID_NICKNAME_REGEX, user_nickname):
        return False
    return True


def is_valid_phone_number(user_phone_number):
    VALID_PHONE_NUMBER_REGEX = r"^[0-9]{11}$"
    if not re.fullmatch(VALID_PHONE_NUMBER_REGEX, user_phone_number):
        return False
    return True


def is_valid_email(user_email):
    VALID_EMAIL_REGEX = "^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9._-]@[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]\\.[a-zA-Z]{2,63}$"
    if not re.fullmatch(VALID_EMAIL_REGEX, user_email):
        return False
    return True


def is_valid_device_alias(device_alias, min_size, max_size):
    VALID_DEVICE_ALIAS_REGEX = r"^[a-zA-Z0-9_-]{" + f"{min_size},{max_size}" + "}$"
    if not re.fullmatch(VALID_DEVICE_ALIAS_REGEX, device_alias):
        return False
    return True
