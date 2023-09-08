#!/venv/bin/python3

"""Decorator to validate a schema with a request object"""
from flask import request

from functools import wraps
from jsonschema import Draft202012Validator
from api.v1.utils.schema.resolver import register


def isvalid(uri_ref):
    """checks if the request object of a particular
    request has the correct decorator
    """
    def decorator_isvalid(f):
        @wraps(f)
        def wrapper_function(*args, **kwargs):
            body = request.get_json()
            validator = Draft202012Validator(
                {"type": "object",
                 "additionalProperties": {"$ref": f"{uri_ref}"}
                 },
                registry=register
            )
            validator.validate(body)
            return f(*args, **kwargs)
        return wrapper_function
