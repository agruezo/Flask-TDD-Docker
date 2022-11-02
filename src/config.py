import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    sa_url = os.environ.get("DATABASE_URL")

    if sa_url is not None and sa_url.startswith("postgres://"):
        sa_url = sa_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = sa_url
