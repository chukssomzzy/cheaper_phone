#!/usr/bin/env -S venv/bin/python3
"""Register user routes"""

from flask import redirect, render_template
from models import storage
from web_dynamics.views import web_dynamics
from web_dynamics.utils.forms.register_customer import RegistrationForm


@web_dynamics.route("/register", methods=["GET", "POST"],
                    strict_slashes=True)
def register_customer():
    """Takes form data then register a user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.data)
        return redirect("/")
    return render_template("pages/register.html", form=form,
                           register="register")
