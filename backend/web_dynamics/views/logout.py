#!/usr/bin/env -S venv/bin/python3
"""Logout view"""
from flask import redirect, url_for
from flask_login import login_required, logout_user
from web_dynamics.views import web_dynamics


@web_dynamics.route("/logout", strict_slashes=False)
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for(".get_home"))
