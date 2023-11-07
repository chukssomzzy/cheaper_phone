#!/usr/bin/env -S venv/bin/python3
""" Render content in user cart """
from uuid import uuid4
from flask import render_template
from models import storage

from web_dynamics.views import web_dynamics


@web_dynamics.route("/customer/cart", methods=["GET"], strict_slashes=False)
def get_user_cart():
    """Render content in user cart"""
    return render_template("pages/cart.html", cart="cart", cache_id=uuid4())
