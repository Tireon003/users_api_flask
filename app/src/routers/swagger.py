from flask import Flask, Response
from flask_swagger_ui import get_swaggerui_blueprint

from app.config import Settings


def setup_swagger(app: Flask, settings: Settings) -> None:
    """
    Swagger configuration setup for Flask application.
    """

    SWAGGER_API_URL = settings.SWAGGER_API_URL
    PATH_TO_DOCS = settings.PATH_TO_DOCS

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_API_URL,
        PATH_TO_DOCS,
        config={"app_name": "User Management API"},
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_API_URL)

    @app.route(PATH_TO_DOCS)
    def serve_openapi() -> Response:
        with open(PATH_TO_DOCS.lstrip("/"), "r") as f:
            return Response(
                response=f.read(),
                mimetype="application/yaml",
                status=200,
            )
