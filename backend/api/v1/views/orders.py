#!/usr/bin/env -S venv/bin/python3
"""Orders endpoint"""
from flask import request
from flask_jwt_extended import current_user, jwt_required
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.views import api_view
from models import storage


@api_view.route("/user/orders", strict_slashes=False)
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
            "User", "Order", customer.id, action="count")
        if isinstance(count, int):
            pages = int(count / limit)
        orders = []
        for order in storage.page_join("User", "Order", customer.id,
                                       limit=limit, page=page,
                                       order_by=order_by).values():
            order_dict = order.to_dict()
            order_dict["status"] = str(order_dict["status"])
            items = []
            for order in order.items:
                order_dict = order.to_dict()
                order_dict["product"] = order.product.to_dict()
                items.append(order_dict)
            order_dict["items"] = items
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
