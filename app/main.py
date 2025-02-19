from flask import Flask
import logging

from app.config import Settings
from app.src.core import db
from app.src.routers import users_router, setup_swagger


def init_logging(settings: Settings) -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


def create_app(settings: Settings) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL
    # init app to db
    db.init_app(app)
    # registration routers
    app.register_blueprint(users_router)
    # init Swagger
    setup_swagger(
        app=app,
        settings=settings,
    )
    return app


if __name__ == "__main__":
    settings = Settings()
    init_logging(settings)
    app = create_app(settings)
    app.run(
        host=settings.API_HOST,
        port=settings.API_PORT,
        debug=settings.IS_DEBUG,
    )
