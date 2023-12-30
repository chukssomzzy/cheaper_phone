#!/usr/bin/env -S venv/bin/python3
"""Defines home route for web_dynamics"""
from os import getenv
from uuid import uuid4

from flask import render_template, request, session
from models import storage

from web_dynamics.views import web_dynamics
api_url = getenv("API_URL")


@web_dynamics.route("/", methods=["GET"], strict_slashes=False)
def get_home():
    """Renders the index route"""
    products = storage.page_all("Product", order_by="created_at")
    all_products = storage.page_all("Product", limit=50, order_by="name")
    return render_template('pages/index.html', products=products,
                           all_products=all_products,
                           cache_id=str(uuid4()), template="index", api_url=api_url)
