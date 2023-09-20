#!/usr/bin/env venv/bin/activate
"""Add a shipping_address for a user"""
from flask import abort, request, url_for
from flask_jwt_extended import current_user, jwt_required

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from models import storage
from models.shipping_address import ShippingAddress

# Todo
# add a shipping address
# remove address
# delete address
# make default address


@api_view.route("/customer/address", methods=["Post"], strict_slashes=False)
@jwt_required()
@isvalid("shipping_address_schema.json")
def post_address():
    """
    add a shipping address to user
    Args
    None
    args
    None
    Response:
        array of all address in the user object
    Raises:
        400: bad request
        401: unauthorised user or not authenticated
    """
    customer = current_user
    body = request.get_json()
    body["user_id"] = customer.id
    if body.get("default"):
        ShippingAddress.change_default(customer.id)
    shipping_address = storage.create("ShippingAddress", **body)
    if not shipping_address:
        abort(400)
    storage.save()
    addresses = []
    for address in customer.addresses:
        address_dict = address.to_dict()
        address_dict["address_type"] = str(address.address_type)
        addresses.append(address_dict)
    return {"addresses": addresses}


@api_view.route("/customer/addresses", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_all_address():
    """Get all shipping address
    Args:
        None
    args:
        None
    Response:
        list of all shipping addresss in a dict
    Raises:
        401: AUthorized access

    """
    customer = current_user
    addresses = []

    for address in customer.addresses:
        address_dict = address.to_dict()
        address_dict["address_type"] = str(address.address_type)
        addresses.append(address_dict)
    return {"addresses": addresses}


@api_view.route("/customer/addresses/<int:address_id>", methods=["DELETE"],
                strict_slashes=False)
@jwt_required()
def delete_address(address_id):
    """Delete address from a user
    Args
        address_id (int): identifies the user
    args
        None
    Response
        No response and 204 status code
    Raises
        404: add doesn't exit
        401: authorized access
    """
    customer = current_user
    address = storage.filter(
        "ShippingAddress", id=address_id, user_id=customer.id)
    if not address:
        abort(404)
    key = "ShippingAddress" + "." + str(address_id)
    storage.delete(address[key])
    storage.save()
    return {}, 204


@api_view.route("/customer/addresses/<int:address_id>", methods=["PUT"],
                strict_slashes=False)
@jwt_required()
@isvalid("update_shipping_address_schema.json")
def update_address(address_id):
    """update a user address
    Args
        address_id identify the shipping address table to update
    args:
        None
    Response
        the dict representation of the updated adddress
    Raises
        400: no request content
        404: No address is identified with the address_id
        401: unauthorized access to route
    """
    customer = current_user
    address = storage.filter(
        "ShippingAddress", id=address_id, user_id=customer.id)
    if not address:
        abort(404)
    shipping_data = request.get_json()
    if shipping_data.get("default"):
        ShippingAddress.change_default(customer.id)
    if not shipping_data:
        raise InvalidApiUsage("Must contain some data to update")
    key = "ShippingAddress" + "." + str(address_id)
    address = address[key]
    address.update(**shipping_data)
    storage.save()
    return address.to_dict()


@api_view.route("/customer/addresses/<int:address_id>", methods=["GET"],
                strict_slashes=False)
@jwt_required()
def get_address_by_id(address_id):
    """Get a single address by id
    Args
        address_id (str): uniquely identifies the address
    args
        none
    Response
        address obj dict representation
    Raises
        401: unauthorized access to route
        400: bad request
        404: address doesn't exit with the uuid
    """
    customer = current_user
    address = storage.filter(
        "ShippingAddress", id=str(address_id), user_id=customer.id)
    if not address:
        InvalidApiUsage(
            f"Address with {address_id} doesn't exit", status_code=404)
    key = "ShippingAddress" + "." + str(address_id)
    address = address[key]
    address = address.to_dict()
    address["address_type"] = str(address.get("address_type"))
    address_dict = {}
    address_dict["address"] = address
    address_dict["actions"] = []
    address_dict["actions"].append({"deleteAddress": url_for(
        ".delete_address", address_id=address["id"], _external=True)})
    address_dict["actions"].append({"updateAddress": url_for(
        ".update_address", address_id=address["id"], _external=True)})

    return address_dict
