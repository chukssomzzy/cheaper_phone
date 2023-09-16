#!/usr/bin/env -S venv/bin/python3

"""Api endpoints related to cart"""
from flask_jwt_extended import jwt_required, current_user
from api.v1.views import api_view
from models import storage

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
    customer = storage.get("User", current_user.id)
    if not customer:
        return {}, 204
    cart = customer.cart
    if cart:
        cart_dict = cart.to_dict()
    else:
        cart_dict = {}
    cart_dict["items"] = []
    if cart:
        for productDetail in cart.items:
            item_dict = productDetail.to_dict()
            if productDetail.products:
                item_dict["product"] = productDetail.product.to_dict()
            cart_dict.append(item_dict)
    cart_dict["actions"] = ["add_to_cart", "remove_from_cart",
                            "delete_from_cart", "reduce_quantity_item"]
    return cart_dict
