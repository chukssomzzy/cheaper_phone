#!/usr/bin/env -S venv/bin/python3

"""Api endpoints related to cart"""
from flask_jwt_extended import jwt_required
from api.v1.views import api_view

# Todos
# add to cart (product)
# remove from cart (product)
# clear cart   all (product)


@api_view.route("/customer/cart", strict_slashes=False)
@jwt_required()
def get_cart():
    """Get all cartItems
    Args
        None
    args
        None
    Response
        dict representaion of cart items
    Raises
    """
    customer = current_user
    cart = customer.cart
    for product in customer.cart.items:
        product =
