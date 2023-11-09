#!/usr/bin/env -S venv/bin/python3
""" Render content in user cart """
from os import getenv
from uuid import uuid4
from flask import render_template

from web_dynamics.views import web_dynamics
api_url = getenv("ECOMMERCE_API_URL")


@web_dynamics.route("/customer/cart", methods=["GET"], strict_slashes=False)
def get_user_cart():
    """Render content in user cart"""
    return render_template("pages/cart.html", cart="cart", cache_id=uuid4(), api_url=api_url)
