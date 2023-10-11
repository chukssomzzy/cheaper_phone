#!/usr/bin/env -S venv/bin/python3

"""Defines app context for views"""
from datetime import timedelta
from os import getenv

from flask import Flask, make_response
from flask_jwt_extended import JWTManager
from werkzeug import exceptions

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.views import api_view
from models import storage
import stripe


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = getenv("APP_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
stripe.api_key = getenv("STRIPE_SECRET_KEY")
stripe_obj = stripe

jwt = JWTManager(app)

app.register_blueprint(api_view)


@jwt.user_identity_loader
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


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """A callback that lookup a particular user based on
    jwt_data
    Args:
        _jwt_header: contains jwt byte
        jwt_data: contains data contain in jwt
    """
    id = jwt_data["sub"]
    return storage.get("User", id)


@app.teardown_appcontext
def teardown_storage(exception):
    """Would request a database session for each request"""
    storage.close()


@app.errorhandler(InvalidApiUsage)
def invalid_api_usage(e):
    """ Handles all invalid api error"""
    return make_response(e.to_dict(), e.status_code)


@app.errorhandler(exceptions.NotFound)
def handle_not_found(e):
    """Handle resource not found for the entire app
    Args:
        e (obj): error obj
    response:
        error: str
    """
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    port = int(getenv("ECOMMERCE_PORT", 5000))
    host = getenv("ECOMMERCE_HOST", "0.0.0.0")
    threaded = getenv("ECOMMERCE_THREAD", False)
    debug = False
    if getenv("ECOMMERCE_ENV") == "DEV":
        debug = True
    app.run(host=host, port=port, threaded=threaded, debug=debug)
