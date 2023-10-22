#!/usr/bin/env -S venv/bin/python3
"""Render web dynamics for the application"""

from os import getenv
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def get_home():
    """Renders the index route"""
    return render_template('index.html')


if __name__ == "__main__":
    port = int(getenv("ECOMMERCE_WEB_PORT", 3000))
    host = getenv("ECOMMERCE_HOST", "0.0.0.0")
    threaded = getenv("ECOMMERCE_WEB_THREAD", False)
    debug = False
    if getenv("ECOMMERCE_ENV") == "DEV":
        debug = True
    app.run(host=host, port=port, threaded=threaded, debug=True)
