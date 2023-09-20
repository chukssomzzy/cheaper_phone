#!/usr/bin/env -S venv/bin/python3
"""Orders endpoint"""
from flask import request, url_for
from flask_jwt_extended import current_user, jwt_required
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.jwt.is_admin import is_admin
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
        raise InvalidApiUsage("wrong type must by a integer")
    except ZeroDivisionError:
        raise InvalidApiUsage('integer must be greater than 0')


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
    for user_product in user_cart_products.values():
        product = user_product.product
        total_amount = total_amount + \
            (product.price * user_product.quantity)
    order = Order(user_id=customer.id,
                  total_amount=total_amount,
                  shipping_address_id=address.id)
    order.save()
    order_id = order.id
    for user_product in user_cart_products.values():
        order_item = OrderItem(
            order_id=order_id, product_id=user_product.product_id,
            quantity=user_product.quantity)
        order_item.save()
        storage.delete(user_product)
    storage.save()
    order_dict = order.to_dict()
    order_dict["id"] = order.id
    return order_dict, 201


@api_view.route("/customer/orders/<int:order_id>/cancel",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
def cancel_order(order_id):
    """cancel an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found
    """
    customer = current_user
    order = storage.filter("Order", user_id=customer.id, id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.cancelled
    storage.save()
    order_dict = order.to_dict()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/process",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def process_order(order_id, user_id):
    """Process an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.processing
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/ship",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def ship_order(order_id, user_id):
    """ship an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.shipped
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/deliver",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def deliver_order(order_id, user_id):
    """deliver an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.delivered
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/return",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def return_order(order_id, user_id):
    """return an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.returned
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/refund",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def refund_order(order_id, user_id):
    """refund an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.refunded
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/hold",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def hold_order(order_id, user_id):
    """hold an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.on_hold
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/ready_for_pickup",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def pickup_order(order_id, user_id):
    """pickup status an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.ready_for_pickup
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/backorder",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def back_order(order_id, user_id):
    """backorder an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.backordered
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/partial_ship",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def partial_ship_order(order_id, user_id):
    """partial ship  an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.partial_shipment
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/process_delay",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def delay_order(order_id, user_id):
    """delay  an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.process_delay
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/payment_pending",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def payment_pending(order_id, user_id):
    """payment pending for an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.payment_pending
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict


@api_view.route("/order/<int:order_id>/user/<uuid:user_id>/payment_failed",
                methods=["PUT"], strict_slashes=False)
@jwt_required()
@is_admin
def payment_failed(order_id, user_id):
    """payment failed for an order
    Args
        order_id (int): identifies the order_id
    args
        None
    Response
        dict representation of order
    Raises
        401: unauthorised access
        400: bad request
        404: order not found

    """
    order = storage.filter("Order", user_id=str(user_id), id=int(order_id))
    if not len(order):
        raise InvalidApiUsage("order doesn't exit", status_code=404)
    order_key = "Order" + "." + str(order_id)
    order = order[order_key]
    order.status = order.status.payment_failed
    order_dict = order.to_dict()
    storage.save()
    order_dict["status"] = str(order.status)
    return order_dict
