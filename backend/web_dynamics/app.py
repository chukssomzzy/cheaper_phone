#!/usr/bin/env -S venv/bin/python3
"""Render web dynamics for the application"""

from os import getenv

from flask import Flask
from flask_login import LoginManager
from models import storage
from flask_wtf.csrf import CSRFProtect

from web_dynamics.views import web_dynamics

app = Flask(__name__)
app.secret_key = getenv("APP_SECRET_KEY")
login_manager = LoginManager()
csrf = CSRFProtect(app)
login_manager.init_app(app)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.register_blueprint(web_dynamics)


@login_manager.user_loader
def load_user(user_id):
    """Loads user from the db"""
    return storage.get("User", user_id)


@app.teardown_appcontext
def tear_down(error):
    """Get a new session from session factory"""
    storage.close()


if __name__ == "__main__":
    port = int(getenv("WEB_PORT", 5001))
    host = getenv("WEB_HOST", "0.0.0.0")
    threaded = getenv("WEB_THREAD", False)
    debug = False
    if getenv("ENVIRONMENT") == "DEV":
        debug = True
    app.run(host=host, port=port, threaded=threaded, debug=debug)
