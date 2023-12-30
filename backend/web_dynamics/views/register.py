#!/usr/bin/env -S venv/bin/python3
"""Register user routes"""

from os import getenv

import stripe
from flask import redirect, render_template
from models import storage

from web_dynamics.utils.forms.register_customer import RegistrationForm
from web_dynamics.views import web_dynamics

stripe.api_key = getenv("STRIPE_SECRET_KEY")
api_url = getenv("API_URL")


@web_dynamics.route("/register", methods=["GET", "POST"],
                    strict_slashes=True)
def register_customer():
    """Takes form data then creates a user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        if "csrf_token" in form.data:
            del form.data["csrf_token"]
            customer = stripe.Customer.create(
                email=form.data["email"],
                idempotency_key=form.data["username"])
            customer_data = form.data.copy()
            customer_data["stripe_customer_id"] = customer["id"]
            user = storage.create("User", **customer_data)
            storage.save()
            user.create_cart()
            return redirect("/")
    return render_template("pages/register.html", form=form,
                           register="register", api_url=api_url)
