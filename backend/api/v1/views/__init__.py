from flask import Blueprint

"""Defines api_view blueprint"""
api_view = Blueprint("api_view", __name__,
                     url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.products import *
from api.v1.views.categories import *
from api.v1.views.customers import *
from api.v1.views.orders import *
from api.v1.views.cart import *
