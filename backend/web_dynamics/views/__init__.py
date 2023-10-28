#!/usr/bin/env venv/bin/python3

"""Defines web_dynamics blueprint"""
from flask import Blueprint

web_dynamics = Blueprint("web_dynamics", __name__)
from web_dynamics.views.index import * 
from web_dynamics.views.products import * 
from web_dynamics.views.usercart import *
from web_dynamics.views.register import *
