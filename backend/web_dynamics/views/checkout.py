#!/usr/bin/env -S venv/bin/python3
"""Checkout page"""

from os import getenv

import stripe
from flask import abort, redirect, request, session, url_for
from flask_login import current_user, login_required

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from models import storage
from models.order_items import OrderItem
from models.orders import Order, statusEnum
from web_dynamics.views import web_dynamics

stripe.api_key = getenv("STRIPE_SECRET_KEY")


@web_dynamics.route("/customer/order/checkout", strict_slashes=False)
@login_required
def checkout():
    """Checkout route with stripe"""
    customer = current_user
    line_items = []
    checkout_session = {}
    if not customer.cart.items:
        abort(400)
    if not session.get("checkout_session") or not session.get("order_id"):
        for item in customer.cart.items:
            line_item = {}
            if not item.product.stripe_products_id:
                line_item["price_data"] = {}
                line_item["price_data"]["currency"] = "NGN"
                line_item["price_data"]["product_data"] = {}
                line_item["price_data"]["product_data"]["name"] = item.product\
                    .name
                line_item["price_data"]["product_data"]["description"] = item\
                    .product.description
                line_item["price_data"]["product_data"]["images"] = [
                    image.image_url for image in item.product.images]
                line_item["price_data"]["unit_amount"] = int(
                    item.product.price) * 100
            else:
                line_item["price"] = item.product.stripe_products_id
            line_item["quantity"] = item.quantity
            line_items.append(line_item)
        checkout_settings = {}
        checkout_settings["line_items"] = line_items
        checkout_settings["mode"] = "payment"
        checkout_settings["success_url"] = url_for(".get_home", _external=True)
        checkout_settings["client_reference_id"] = customer.id
        checkout_settings["currency"] = "NGN"
        checkout_settings["customer"] = customer.stripe_customer_id
        checkout_settings["shipping_address_collection"] = {}
        checkout_settings["shipping_address_collection"]["allowed_countries"] \
            = ["NG"]
        checkout_session = stripe.checkout.Session.create(
            **checkout_settings)
        session["checkout_session"] = checkout_session.id
        order_dict = {"user_id": customer.id, "total_amount": customer.cart.total_items,
                      "stripe_orders_id": checkout_session.id}
        order = Order(**order_dict)
        order.save()
        order_id = order.id
        for item in customer.cart.items:
            order_item = {"order_id": order_id, "product_id": item.product.id}
            order_item = OrderItem(**order_item)
            order.items.append(order_item)
        storage.save()
        session["order_id"] = order_id
    else:
        checkout_session = stripe.checkout.Session.retrieve(
            session["checkout_session"])

    redirect_url = checkout_session['url']
    return redirect(redirect_url)


@web_dynamics.route("/customer/order/success", strict_slashes=False)
@login_required
def checkout_success():
    """Checkout successful page"""
    session_id = request.args.get("session_id")
    customer = current_user
    if not session_id or not session["order_id"]:
        abort(400)
    checkout_session = stripe.checkout.Session.retrieve(
        session_id, expand=["line_items"])
    shipping_address = checkout_session["customer_details"]["address"]
    shipping_address_data = {}
    if not shipping_address:
        abort(400)
    shipping_address_data["user_id"] = customer.id
    shipping_address_data["address_line1"] = shipping_address["line1"]
    shipping_address_data["city"] = shipping_address["city"]
    shipping_address_data["postal_code"] = shipping_address["postal_code"]
    shipping_address_data["country"] = shipping_address["country"]
    if shipping_address.get("line2"):
        shipping_address_data["address_line2"] = shipping_address["line2"]
    shipping_address_data["state_province"] = shipping_address["state"]
    order_id = session["order_id"]
    order = storage.get("Order", order_id)
    if checkout_session["payment_status"] == "paid":
        order.update(status=statusEnum.processing)
        for item in customer.cart.items:
            item.delete()
        storage.save()
        del session["order_id"]
        del session["checkout_session"]
    return redirect(url_for(".get_home", _anchor="#success"))
