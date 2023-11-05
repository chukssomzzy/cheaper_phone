#!/usr/bin/env -S venv/bin/python3

"""Defines app context for views"""
from datetime import timedelta
from os import getenv

from flasgger import Swagger
from flask import Flask, make_response
from flask_jwt_extended import JWTManager
from werkzeug import exceptions

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.views import api_view
from models import storage
from flask_cors import CORS

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = getenv("APP_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


jwt = JWTManager(app)

app.register_blueprint(api_view)
template = {
    "info": {
        "title": "Cheaper Phone Api",
        "version": "1.0.0",
        "description": "Cheaper Phone Api Endpoints",
        "termsOfService": "",
        "contact": {
            "name": "somzzy",
            "url": "https://github.com/chukssomzzy/cheaper_phone/issues",
            "email": "chukssomzzy@gmail.com"
        }
    },
    "host": getenv("APP_HOST", "http://0.0.0.0:5000"),
    "schemas": ["https", "http"],
    "basePath": "/api/v1",
    "swagger": "2.0"
}
swagger_config = {
    "headers": [

    ],
    "specs": [
        {
            "endpoint": "docs",
            "route": "/api/v1/docs_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/v1/docs/"
}
swagger = Swagger(app,
                  config=swagger_config,
                  template=template)


@ jwt.user_identity_loader
def user_identity_lookup(user):
    """Takes what passed to create jwt identity and
    return a seriliazabe version that can be used to lookup
    the user
    Args:
        User: sqlalchemy obj of user
    Returns:
        user's id
    """
    if isinstance(user, str):
        return user
    return user.id


@ jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """A callback that lookup a particular user based on
    jwt_data
    Args:
        _jwt_header: contains jwt byte
        jwt_data: contains data contain in jwt
    """
    id = jwt_data["sub"]
    return storage.get("User", id)


@ app.teardown_appcontext
def teardown_storage(exception):
    """Would request a database session for each request"""
    storage.close()


@ app.errorhandler(InvalidApiUsage)
def invalid_api_usage(e):
    """ Handles all invalid api error"""
    return make_response(e.to_dict(), e.status_code)


@ app.errorhandler(exceptions.NotFound)
def handle_not_found(e):
    """Handle resource not found for the entire app
    Args:
        e (obj): error obj
    response:
        error: str
    """
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    port = int(getenv("ECOMMERCE_API_PORT", 5000))
    host = getenv("ECOMMERCE_API_HOST", "0.0.0.0")
    threaded = getenv("ECOMMERCE_API_THREAD", False)
    debug = False
    if getenv("ECOMMERCE_ENV") == "DEV":
        debug = True
    app.run(host=host, port=port, threaded=threaded, debug=debug)
