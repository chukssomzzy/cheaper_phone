#!/usr/bin/env -S venv/bin/python3

"""Api endpoints related to cart"""
from flask import url_for
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import and_
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.views import api_view
from models.user_cart import UserCart
from models import storage
from models.user_cart_products import UserCartProduct

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
            cart_dict["items"].append(item_dict)
    return cart_dict


@ api_view.route("/customer/cart/<uuid:product_id>", methods=["PUT"], strict_slashes=False)
@ jwt_required()
def add_product_to_cart(product_id):
    """Takes a uuid a uuuid and add the item identifies by it to cart
    Args:
        product_id (str): identifies the product to add to cart
    args:
        None
    Response:
        usercart object
    Raise:
        400 badrequest
        404 product doesn't exit
        401 authorised accesss
    """
    customer = current_user
    product = storage.get("Product", str(product_id))
    if not product:
        raise InvalidApiUsage(
            "Product you are trying to add to cart doesn't exit",
            status_code=404)
    if not customer.cart:
        user_cart = UserCart(user_id=customer.id)
        customer.cart = user_cart
        storage.save()
    else:
        user_cart = customer.cart
    user_cart_product = storage.session.query(UserCartProduct)\
        .filter_by(user_cart_id=user_cart.id,
                   product_id=product.id).one_or_none()
    if not user_cart_product:
        user_cart_product = storage.create(
            "UserCartProduct", user_cart_id=user_cart.id,
            product_id=product.id)
        user_cart.items.append(user_cart_product)
    else:
        user_cart_product.increase_quantity()
    storage.save()
    customer_dict = customer.to_dict()
    customer_dict["cart"] = user_cart.to_dict()
    product_items = []
    for item in customer.cart.items:
        product_dict = item.to_dict()
        product_dict["product"] = item.product.to_dict()
        product_items.append(product_dict)
    customer_dict["cart"]["items"] = product_items
    return customer_dict, 200


@api_view.route("/customer/cart/<uuid:product_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def remove_product_from_cart(product_id):
    """Takes a product id and removed the identified item from
    cart
    Args:
        product_id: identifies a product in cart
    args:
        None
    Response:
        dict representation of the current cart
    Raises:
        400 bad request
        401 authorised access or jwt expired
        404 product is not in cart
        404 no such product in database
    """
    product = storage.get("Product", product_id)
    return product_id
    "
