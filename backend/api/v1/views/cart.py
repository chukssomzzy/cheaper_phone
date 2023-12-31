#!/usr/bin/env -S venv/bin/python3

"""Api endpoints related to cart"""
from flasgger import swag_from
from flask import url_for
from flask_jwt_extended import current_user, jwt_required

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.views import api_view
from api.v1.views.documentation.cart import (add_product_to_cart_spec,
                                             get_cart_spec,
                                             remove_product_from_cart_spec, delete_from_cart_spec)
from models import storage
from models.user_cart import UserCart
from models.user_cart_products import UserCartProduct

# Todos
# add to cart (product)
# remove from cart (product)
# clear cart   all (product)


@api_view.route("/customer/cart", strict_slashes=False)
@jwt_required()
@swag_from(get_cart_spec)
def get_cart():
    """Get all cartItems
    Args:
        None
    args:
        None
    Response:
        dict representaion of cart items
    Raises:
        """
    customer = storage.get("User", current_user.id)
    if not customer:
        return {}, 204
    cart = customer.cart
    cart_dict = {}
    if cart:
        cart_dict["data"] = cart.to_dict()
        cart_dict["data"]["total"] = cart.total_items
    else:
        raise InvalidApiUsage(
            "customer needs to first create a cart", status_code=404)
    cart_dict["items"] = []
    if cart:
        for item in cart.items:
            item_dict = {}
            item_dict = item.to_dict()
            item_dict["product"] = item.product.to_dict()
            if item.product.images:
                item_dict["product"]["image"] = item.product.image.to_dict()
            cart_dict["items"].append(item_dict)
    return cart_dict


@ api_view.route("/customer/cart/<uuid:product_id>",
                 methods=["POST"], strict_slashes=False)
@ jwt_required()
@swag_from(add_product_to_cart_spec)
def add_product_to_cart(product_id):
    """Takes a uuid and add the item identified  to cart
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
    customer_dict = {}
    customer_dict["customer"] = customer.to_dict()
    customer_dict["cart"] = {}
    user_cart.id
    customer_dict["cart"]["data"] = user_cart.to_dict()
    customer_dict["cart"]["data"]["total_price"] = user_cart.total_items
    product_items = []
    for item in customer.cart.items:
        item.product
        product_dict = item.to_dict()
        product_dict["subtotal"] = item.total
        product_dict["product"]["image"] = item.product.image.to_dict()
        if item.product.image:
            product_dict["product"]["image"] = item.product.image.to_dict()
        product_items.append(product_dict)
    customer_dict["cart"]["items"] = product_items
    return customer_dict, 200


@api_view.route("/customer/cart/<uuid:product_id>",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@swag_from(remove_product_from_cart_spec)
def remove_product_from_cart(product_id):
    """Takes a product id and remove the identified item from
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
    product = storage.get("Product", str(product_id))
    if not product:
        raise InvalidApiUsage(
            "product_id doesn't identify a product", status_code=404)

    customer = current_user
    if not customer.cart:
        raise InvalidApiUsage("you don't have anything in your cart first add \
                              product to cart", status_code=400, payload={
            "add_to_cart": url_for(".add_product_to_cart",
                                   product_id=str(product_id), _external=True),
            "methods": ["PUT"]})
    user_cart = customer.cart
    user_cart_product = storage.session.query(UserCartProduct).filter_by(
        user_cart_id=user_cart.id, product_id=product.id).one_or_none()
    if not user_cart_product:
        raise InvalidApiUsage(
            f"You dont have product with {product_id} in cart", payload={
                "add_to_cart": url_for(".add_product_to_cart",
                                       product_id=str(product_id),
                                       _external=True),
                "methods": ["POST"]})
    user_cart_product.decrease_quantity()
    storage.save()
    customer_dict = {}
    customer.id
    customer_dict['customer'] = customer.to_dict()
    customer_dict['cart'] = {}
    user_cart.id
    customer_dict["cart"]["data"] = user_cart.to_dict()
    customer_dict["cart"]["data"]["total_price"] = user_cart.total_items
    product_items = []
    for item in customer.cart.items:
        item.product
        item.product.brand
        product_dict = item.to_dict()
        product_dict["product"]["image"] = item.product.image.to_dict()
        product_dict["subtotal"] = item.total
        product_items.append(product_dict)
    customer_dict["cart"]["items"] = product_items
    return customer_dict, 200


@api_view.route("/customer/cart/<uuid:product_id>",
                methods=["DELETE"], strict_slashes=False)
@jwt_required()
@swag_from(delete_from_cart_spec)
def delete_from_cart(product_id):
    """delete a product from cart
    Args:
        product_id (str): unique identifies the product to remove from cart
    args:
        None
    Response:
        Return an empty object and 204 status code
    Raises:
        400 bad request no product id in argument or product id is not a string
        401: unauthorized access to these route
        404: product cannot be found
        404: the current user doesn't have a cart
    """
    product = storage.get("Product", str(product_id))
    if not product:
        raise InvalidApiUsage("No such product exits")
    customer = current_user
    if not customer.cart:
        raise InvalidApiUsage("You need to add something to cart to remove",
                              payload={"add_to_cart": url_for(
                                  ".add_product_to_cart",
                                  product_id=product.id, _external=True),
                                  "methods": ["POST"]})
    user_cart = customer.cart
    user_cart_product = storage.session.query(UserCartProduct).filter_by(
        user_cart_id=user_cart.id, product_id=product.id).one_or_none()
    if not user_cart_product:
        raise InvalidApiUsage(f"product f{product.id} is not in user cart",
                              payload={"add_to_cart":
                                       url_for(".add_product_to_cart",
                                               product_id=product.id,
                                               _external=True)})
    user_cart_product.delete()
    storage.save()
    cart_dict = {}
    customer.id
    user_cart.id
    cart_dict["customer"] = customer.to_dict()
    cart_dict["cart"] = {}
    cart_dict["cart"]["data"] = user_cart.to_dict()
    cart_dict["cart"]["data"]["total_price"] = user_cart.total_items
    cart_dict["cart"]["items"] = []
    for item in customer.cart.items:
        item.product
        item.product.brand
        item_dict = item.to_dict()
        item_dict["product"]["image"] = item.product.image.to_dict()
        item_dict["subtotal"] = item.total
        cart_dict["cart"]["items"].append(item_dict)

    return cart_dict, 200
