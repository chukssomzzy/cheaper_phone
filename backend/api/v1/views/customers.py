#!/usr/bin/env -S venv/bin/python3
"""Contains all users related endpoints"""
from flask import jsonify, request, url_for
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required, current_user)
from sqlalchemy.exc import IntegrityError

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from models import storage
from models.users import User
from app import stripe_obj


@api_view.route("/customer/register", methods=["POST"])
@isvalid("customer_schema.json")
def register_customer():
    """Register a customer to the db
    Args:
        None
    args;
        None
    Response:
        register customer information and id
    Raises:
        400 bad request, integrity error username is already taken
    """
    try:
        customer_data = request.get_json()
        customer = User(**customer_data)
        storage.new(customer)
        storage.save()
        return ({"customer": customer.id}), 201
    except IntegrityError:
        raise InvalidApiUsage(
            "Username or email is already taken pick another one")


@api_view.route("/customer/login", methods=["POST"], strict_slashes=False)
def login():
    body = request.get_json()
    user = None
    if "username" in body:
        user = storage.session.query(User).filter_by(
            username=body["username"]).one_or_none()
    if "email" in body:
        user = storage.session.query(User).filter_by(
            email=body["email"]).one_or_none()
    if not user:
        raise InvalidApiUsage("username is not correct")
    elif not bool(user.check_password(body["password"])):
        raise InvalidApiUsage("password not correct")
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api_view.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get a new access token if the refresh token hasn't expired"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@api_view.route("/customer/profile", strict_slashes=False)
@jwt_required()
def get_profile():
    """Get the profile for the current authenticated user
    Args:
        None
    args:
        None:
    Response:
        actions: all thing the current authenticated user can do
        user: user information address and other related information
    Raise:
        401: unauthenticated to view the route
    """
    customer = current_user
    address = []
    print(current_user)
    if current_user.shipping_address:
        for address in current_user.shipping_address.values():
            address_dict = address.to_dict()
            address.append(address_dict)
    customer_dict = customer.to_dict()
    customer_dict["shipping_address"] = address
    actions = []
    actions.append({"editUser": url_for(".edit_customer", _external=True)})
    actions.append({"changePassword": url_for(
        ".change_password", _external=True)})
    actions.append({"ViewOrder": url_for(".get_user_orders", _external=True)})
    actions.append({"UserCart": url_for(".get_cart", _external=True)})
    res_dict = {"customer": customer_dict, "actions": actions}
    return res_dict


@api_view.route("/user/profile/edit", methods=["PUT"])
@jwt_required()
@isvalid("update_profile_schema.json")
def edit_customer():
    """Edit any profile information
    Args:
        None
    args:
        None
    Response:
        dict changed
    Raises:
        400 bad request
        401 unauthorized

    """
    customer = current_user
    body = request.get_json()
    address = {}
    if "shipping_address" in body:
        address = body["shipping_address"]
        address["user_id"] = str(current_user.id)
        address = storage.create("Address", **address)
        del body["shipping_adress"]
    customer.update(**body)
    storage.save()
    customer_dict = customer.to_dict()
    return customer_dict


@api_view.route("/user/change_password", methods=["PUT"])
@jwt_required()
@isvalid("change_password_schema.json")
def change_password():
    """Change the current user password
    Args:
        None
    args:
        None
    Response:
        No content 204
    Raises:
        401: unauthorized access
        400: badrequest
        400: invalid user_id or password
        204: success
    """
    body = request.get_json()
    customer = current_user
    if body["user_id"] == current_user.id and customer.check_password(
            body["old_password"]):
        customer.password = body["new_password"]
    else:
        InvalidApiUsage(
            "user_id must identify a user and old_password must be the \
user current password")
    storage.save()
    return {}, 204
