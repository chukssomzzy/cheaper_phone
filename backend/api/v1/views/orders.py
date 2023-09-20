#!/usr/bin/env -S venv/bin/python3
"""Orders endpoint"""
from flask import request, url_for
from flask_jwt_extended import current_user, jwt_required
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.views import api_view
from models import storage
from models.order_items import OrderItem
from models.orders import Order

# todos
# create an order
# cancel an order
# delete an order


@api_view.route("/customer/orders", strict_slashes=False)
@jwt_required()
def get_user_orders():
    """Get all orders that have been placed by a user
    Args:
        None
    args:
        page: current page
        limit: number of orders per page
        order_by: what to order the pages by
    Response:
        pagination: information about pagination
        actions: order_by what the orders can be filter_by
    """
    try:
        limit = int(request.args.get("limit", 10))
        page = int(request.args.get("page", 1))
        order_by = request.args.get("order_by", 'created_by')
        order_key = ["created_by", "update_by",
                     "id", "status", "total_amount"]
        if order_by not in order_key:
            order_by = "created_by"
        count = 0
        customer = current_user
        pages = 0

        count = storage.page_join(
            "User", "orders", customer.id, action="count")
        if isinstance(count, int):
            pages = int(count / limit)
        orders = []
        if len(customer.orders):
            for order in storage.page_join("User", "orders", customer.id,
                                           limit=limit, page=page,
                                           order_by=order_by).values():
                order_dict = order.to_dict()
                order_dict["status"] = str(order_dict["status"])
                order_dict["order_items"] = []
                for item in order.items:
                    item_dict = item.to_dict()
                    if item.product:
                        item_dict["product"] = item.product.to_dict()
                    order_dict["order_items"].append(item_dict)
                if order.address:
                    order_dict["address"] = order.address.to_dict()

                orders.append(order_dict)
        res_dict = {}
        res_dict["pagination"] = {'pages': pages, 'limit': limit, 'page': page}
        res_dict["actions"] = []
        res_dict["actions"].append({"order_by": order_key})
        res_dict["orders"] = orders
        return res_dict
    except TypeError:
        InvalidApiUsage("wrong type must by a integer")
    except ZeroDivisionError:
        InvalidApiUsage('integer must be greater than 0')


@api_view.route("/customer/orders/cart/<uuid:cart_id>",
                methods=["POST"], strict_slashes=False)
@jwt_required()
def create_order(cart_id):
    """Takes a cart_id and create a new order with every items
    in the cart remove all items from the cart once order has been successfully
    created
    Args
        cart_id (int): identifies the cart to create order  from
    args
        None
    Response
        json representation of the newly created order
    Raises
        400: bad request
        401: unauthorised access
        404: cart doesn't exist
    """
    customer = current_user
    cart = storage.filter("UserCart", user_id=customer.id, id=str(cart_id))
    if not cart:
        raise InvalidApiUsage(
            f"usercart doesn't exist for {cart_id}", status_code=404)
    cart_key = "UserCart" + "." + str(cart_id)
    cart = cart[cart_key]
    user_cart_products = storage.filter(
        "UserCartProduct", user_cart_id=cart.id)
    if not user_cart_products:
        raise InvalidApiUsage("no products in cart", status_code=404)
    address = customer.get_default_address()
    if not address:
        raise InvalidApiUsage("current customer does not have shipping \
                              address", status_code=404,
                              payload={"createShippingAddress":
                                       url_for(".post_address",
                                               _external=True)})
    total_amount = 0
    product_ids = []
    for user_product in user_cart_products.values():
        product = user_product.product
        product_ids.append(product.id)
        total_amount = total_amount + \
            (product.price * user_product.quantity)
    order = Order(user_id=customer.id,
                  total_amount=total_amount,
                  shipping_address_id=address.id)
    storage.save()
    order_id = order.id
    for product_id in product_ids:
        OrderItem(order_id=order_id, product_id=product_id)
    storage.save()
    order_dict = order.to_dict()
    return order_dict, 201
