#!/usr/bin/env -S venv/bin/python3
"""Checks if the current user is an admin"""


from functools import wraps

from flask_jwt_extended import current_user

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage


def is_admin(f):
    """Wraps function and check if the current_user
    is an admin"""
    @wraps(f)
    def wrapper_is_admin(*args, **kwargs):
        """check if user is admin"""
        if not current_user.role.admin:
            raise InvalidApiUsage("unauthorized access")
        return f(*args, **kwargs)
    return wrapper_is_admin
