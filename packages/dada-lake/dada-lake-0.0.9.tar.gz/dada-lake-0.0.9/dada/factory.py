import os
import logging
import logging.config

import flask
from flask import request, g, make_response
from werkzeug.exceptions import HTTPException
from psycopg2 import IntegrityError, InternalError, ProgrammingError
from celery import Celery
from flask_cors import CORS
from flask_apispec import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_apispec.extension import FlaskApiSpec

# plugins to init
from dada.models.core import db, ma

# resources
from dada.resources.desktops import DESKTOPS_APP
from dada.resources.fields import FIELDS_APP
from dada.resources.files import FILES_APP
from dada.resources.folders import FOLDERS_APP
from dada.resources.me import ME_APP
from dada.resources.tags import TAGS_APP
from dada.resources.users import USERS_APP

import dada_settings
from dada_errors import ERRORS
from dada.queue.core import init_celery
from dada_serde import jsonify

LOGGER = logging.getLogger()

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

app = None


def create_app(app_name=PKG_NAME, **kwargs):
    """Create and configure the Flask application."""
    global app

    if app is None:

        # app configuration
        app = flask.Flask(__name__)
        app.config.from_object("dada_settings")
        logging.config.dictConfig(app.config["LOGGING_CONFIG"])

        # celery
        if kwargs.get("celery"):
            init_celery(kwargs["celery"], app)

        # blueprints
        app.register_blueprint(FIELDS_APP, url_prefix="/fields")
        app.register_blueprint(FILES_APP, url_prefix="/files")
        app.register_blueprint(FOLDERS_APP, url_prefix="/folders")
        app.register_blueprint(DESKTOPS_APP, url_prefix="/desktops")
        app.register_blueprint(ME_APP, url_prefix="/me")
        app.register_blueprint(TAGS_APP, url_prefix="/tags")
        app.register_blueprint(USERS_APP, url_prefix="/users")

        # global configs
        app.url_map.strict_slashes = False

        # plugins
        db.init_app(app)  # sqlalchemy
        ma.init_app(app)  # marshmallow
        CORS(app)  # flask cross origin'

        # flask apispec
        spec = APISpec(
            title="DADA Lake API",
            version=dada_settings.API_VERSION,
            openapi_version="3.0.2",
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )

        app.config.update(
            {
                "APISPEC_SPEC": spec,
                "APISPEC_SWAGGER_URL": app.config["APISPEC_SWAGGER_URL"],
                "APISPEC_SWAGGER_UI_URL": app.config["APISPEC_SWAGGER_UI_URL"],
            }
        )
        docs = FlaskApiSpec(app)

        # register docs for all views
        for key, view in app.view_functions.items():
            bp = key.split(".")[0]
            if key != "static" and not key.startswith("flask-apispec"):
                with app.test_request_context():
                    docs.register(target=view, endpoint=key)

        # healthcheck
        @app.route("/yo", methods=["GET"])
        def yo():
            return make_response("yo", 200)

        # error handling
        @app.errorhandler(401)
        @app.errorhandler(403)
        @app.errorhandler(404)
        @app.errorhandler(409)
        @app.errorhandler(410)
        @app.errorhandler(422)
        @app.errorhandler(500)
        def handle_exceptions(exc):

            headers = {}
            err_name = getattr(exc, "name", None)

            # handle built-in errors
            if ERRORS.get(err_name):

                resp = {
                    "status_code": exc.status_code,
                    "error": exc.name,
                    "message": exc.message,
                }
                response = jsonify(resp)
                response.status_code = exc.status_code
                return response

            elif isinstance(exc, HTTPException):
                body = {
                    "status_code": exc.code,
                    "error": exc.name,
                    "message": exc.get_description(request.environ)
                    .replace("<p>", "")
                    .replace("</p>", ""),
                }
                headers = exc.get_headers(request.environ)

            elif isinstance(exc, ProgrammingError):
                db.session.rollback()
                body = {
                    "status_code": 400,
                    "error": "RequestError",
                    "messgage": str(exc),
                }

            elif isinstance(exc, IntegrityError):
                db.session.rollback()
                body = {
                    "status_code": 409,
                    "error": "ConflictError",
                    "messgage": str(exc),
                }

            elif isinstance(exc, InternalError):
                db.session.rollback()
                body = {
                    "status_code": 500,
                    "error": "InternalServiceError",
                    "messgage": str(exc),
                }

            # TODO: Schema Validation Errors

            else:
                db.session.rollback()
                body = {
                    "status_code": 500,
                    "error": exc.__class__.__name__,
                    "message": str(exc),
                }

            return jsonify(body, status=body.get("status_code"), headers=headers)

        # TODO: Create event stream here!
        @app.after_request
        def after_triggers(response):
            LOGGER.debug(
                f"GOT RESPONSE: {response.__dict__} FROM REQUEST {request.__dict__}"
            )
            return response

        # triggers
        @app.teardown_appcontext
        def shutdown_sessions(exception=None):
            # cleanup session
            db.session.remove()

    return app
