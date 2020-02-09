import pathlib

current_path = pathlib.Path(__file__)
db_path = current_path.parent / "sqlite.db"


class Config:
    DEBUG = False
    SECRET_KEY = "2f807b548e7344cb9fd91b7c33719f4a"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'localhost'
    MAIL_USE_TLC = True
    MAIL_PORT = 587
    MAIL_USERNAME = 'user@example.com'
    MAIL_PASSWORD = 'password'
