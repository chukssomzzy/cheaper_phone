#!/usr/bin/env -S venv/bin/python3
"""Checkout page"""

from os import getenv
import string

from flask_login import current_user, login_required
from web_dynamics.views import web_dynamics

stripe.api_key = getenv("STRIPE_API_KEY")


@web_dynamics.route("/customer/checkout")
@login_required
def checkout():
    """Checkout route with stripe"""
    customer = current_user
    line_items = []

    for item in customer.cart.items:
        line_item = {}
        line_item["price_data"]["currency"] = "NGN"
        line_item["price_data"]["product_data"] = {}
        line_item["price_data"]["product_data"]["name"] = item.product.name
        line_item["price_data"]["product_data"]["description"] = item.product.description
        line_item["price_data"]["product_data"]["images"] = [
            image.image_url for image in item.product.images]
        line_item["price_data"]["unit_amount"] = item.product.price
        line_item["quantity"] = item.quantity
        line_item["adjustable_quantity"]["enabled"] = True
        line_item["adjustable_quantity"]["maximum"] = 20
    checkout_settings = {}
    checkout_settings["line_items"] = line_items
    checkout_settings["mode"] = "payment"
    checkout_settings["return_url"] = url_for(".get_home")
    checkout_settings["cient_reference_id"] = customer.id
    checkout_settings["currency"] = "NGN"
    checkout_settings["customer"] = customer.stripe_id
    checkout_settings["customer_email"] = customer.email
    checkout_session = stripe.checkout.Session.create(**checkout_settings)

    line_items.append(line_item)
