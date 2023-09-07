from os import getenv
from flask import Flask, make_response
from werkzeug import exceptions
from api.v1.utils.invalid_api_error import InvalidApiUsage
from models import storage
from api.v1.views import api_view
"""Defines app context for views"""


app = Flask(__name__)
app.register_blueprint(api_view)


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
