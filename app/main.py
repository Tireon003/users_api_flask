from flask import Flask
import logging

from app.config import settings
from app.src.core import db
from app.src.routers import users_router


def init_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


def create_app() -> Flask:

    app = Flask(__name__)

    # configure flask app config
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL

    # init app to db
    db.init_app(app)

    # registration routers
    app.register_blueprint(users_router)
    return app


if __name__ == "__main__":
    init_logging()
    app = create_app()
    app.run(
        host=settings.API_HOST,
        port=settings.API_PORT,
        debug=settings.IS_DEBUG,
    )
