from flask import Blueprint

"""Defines api_view blueprint"""
api_view = Blueprint("api_view", __name__,
                     url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.products import *