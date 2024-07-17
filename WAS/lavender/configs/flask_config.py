class Config(object):
    import os
    from dotenv import load_dotenv

    load_dotenv()
    ENV = os.getenv("ENV")
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        "userDB": (
            f"mysql+pymysql://{os.getenv('user_DB_USERNAME')}:{os.getenv('user_DB_PASSWORD')}"
            + f"@{os.getenv('user_DB_HOST')}:{os.getenv('user_DB_PORT')}"
            + f"/{os.getenv('user_DB_DATABASE')}"
        ),
        "resultDB": (
            f"mysql+pymysql://{os.getenv('result_DB_USERNAME')}:{os.getenv('result_DB_PASSWORD')}"
            + f"@{os.getenv('result_DB_HOST')}:{os.getenv('result_DB_PORT')}"
            + f"/{os.getenv('result_DB_DATABASE')}"
        ),
    }

    # SQLALCHEMY_DATABASE_URI = (
    #     f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    #     + f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    #     + f"/{os.getenv('DB_DATABASE')}"
    # )


class devConfig(Config):
    Debug = True


class prodConfig(Config):
    Debug = False
