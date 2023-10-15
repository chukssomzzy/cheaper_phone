#!/usr/bin/env venv/bin/python3
"""promotions endpoints"""

from flasgger import swag_from
from flask import abort, request, url_for
from flask_jwt_extended import jwt_required
from models import storage
from models.products import Product
from models.promotions import Promotion, product_promotions

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.jwt.is_admin import is_admin
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from api.v1.views.documentation.promotions import (
    add_promotion_product_spec, delete_promotion_product_spec,
    delete_promotion_spec, get_product_promotions_spec, get_promotions_spec,
    post_promotions_spec, update_promotion_spec)
from api.v1.views.orders import back_order


@api_view.route("/products/<uuid:product_id>/promotions", strict_slashes=False)
@swag_from(get_product_promotions_spec)
def get_product_promotions(product_id):
    """Get promotions for a product that is yet to expire

    args:
        None
    Args:
        product_id (str): uuid for product
    Raises:
        404: product not found
        400: bad request
    Returns:
        serializable list of object containing all promotion yet to expire for
        a product
    """
    product = storage.get("Product", str(product_id))
    if not product:
        InvalidApiUsage("product not found", status_code=404)
    promotions_dict = []
    for promotion in product.promotions:
        if not promotion.is_expired():
            promotions_dict.append(promotion.to_dict())
        else:
            promotion.update(isexpired=True)
            storage.save()

    return {"promotions": promotions_dict}


@api_view.route("/promotions", methods=["POST"], strict_slashes=False)
@jwt_required()
@is_admin
@isvalid("promotion_schema.json")
@swag_from(post_promotions_spec)
def post_promotions():
    """Post a promotions
    args:
        None
    Args:
        None
    Raises:
        401: unauthorized access to route
        400: bad request
    Return:
        id of created promotion
    """
    body = request.get_json()
    promotion = Promotion(**body)

    if not promotion:
        raise InvalidApiUsage(
            "promotion couldn't be created in db", payload=body)
    promotion.save()
    return (promotion.to_dict()), 201


@api_view.route('/promotions/<int:promotion_id>', methods=["DELETE"],
                strict_slashes=False)
@jwt_required()
@is_admin
@swag_from(delete_promotion_spec)
def delete_promotion(promotion_id):
    """Delete a promotions
    args:
        None
    Args:
        None
    Raises:
        401: unauthorised access to route
        400: bad request
    Return:
        No response (204)
    """
    promotion = storage.get("Promotion", promotion_id)

    if not promotion:
        raise InvalidApiUsage("promotion not found", promotion_id)
    storage.delete(promotion)
    return ({}), 204


@api_view.route('/promotions/<int:promotion_id>/products', strict_slashes=False)
@swag_from(get_product_promotions_spec)
def get_product_by_promotions(promotion_id):
    """Get all product with promotion

    args:
        page: page to get from db
        limit: no of obj per page
        order_by: what to order page by
    Args:
        None
    Raises:
        404: promotion not found
        400: bad request
    Returns:
        dict containing product
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        order_by = str(request.args.get("order_by", "created_by"))
        order_bys = ["created_at", "updated_at", "price", "name"]

        if order_by not in order_bys:
            raise InvalidApiUsage("orderby must a string", payload=order_bys)
        obj_count = storage.session.query(Product).join(product_promotions).\
            filter(product_promotions.c.promotion_id ==
                   int(promotion_id)).count()
        pages = obj_count / limit
        endIdx = page * limit if (page * limit) <= obj_count else obj_count
        startIdx = (page - 1) * limit if (page - 1) * limit > endIdx else 0
        promotion = storage.get("Promotions", int(promotion_id))
        if not promotion:
            raise InvalidApiUsage("promotion not found", status_code=404)
        products_dict = []
        for product in storage.session.query(Product).join(product_promotions).\
                filter(product_promotions.c.promotion_id == promotion_id).\
                order_by(getattr(Product, order_by))[startIdx:endIdx]:
            product_dict = product.to_dict()
            products_dict.append(product_dict)
        paginate = {"page": page, "limit": limit,
                    "pages": pages, "order_by": order_bys}
        return ({"pagination": paginate, "products": products_dict})

    except ZeroDivisionError:
        raise InvalidApiUsage("limit must be greater than 0")
    except TypeError:
        raise InvalidApiUsage("limit, page must be an integer type")
    except Exception:
        abort(400)


@api_view.route("/promotions", strict_slashes=False)
@swag_from(get_promotions_spec)
def get_promotions():
    """Get all promotions in a db that has not expired

    args:
        limit: no of items per page
        page: page No to fetch
        order_by: key to order fetched item with
    Args:
        None
    Raises:
        400 bad request
        404: no promotion was found in db
    Return:
        dict containing an array with all the promotions
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        order_by = str(request.args.get("order_by", "created_at"))
        order_bys = ["created_at", "updated_at", "id",
                     "discount", "start_date", "duration"]

        obj_count = storage.count("Promotion")
        pages = obj_count / limit
        endIdx = (page * limit) if (page * limit) <= obj_count else obj_count
        startIdx = (page - 1) * limit if (page - 1) * limit < endIdx else 0
        promotions_dict = {"promotions": [], "pagination": {}}

        for promotion in storage.session.query(Promotion)\
                .filter_by(isexpired=False)\
                .order_by(getattr(Promotion, order_by))[startIdx:endIdx]:
            if not promotion.is_expired():
                promotion_dict = {}
                promotion_dict["data"] = promotion.to_dict()
                promotion_dict["actions"] = []
                promotion_dict["actions"].append(
                    {"getProduct": url_for(".get_product_by_promotions",
                                           promotion_id=promotion.id,
                                           _external=True)})
                promotions_dict["promotions"].append(promotion_dict)
            else:
                promotion.update(is_expired=True)
                storage.save()
        paginate = {"page": page, "limit": limit,
                    "pages": pages, "order_by": order_bys}
        promotions_dict["pagination"] = paginate
        return promotions_dict
    except ZeroDivisionError:
        raise InvalidApiUsage("limit must be greater than zero")
    except TypeError:
        raise InvalidApiUsage(
            "page, limit, order_by must of type integer, integer and string\
respectively")
    except Exception as e:
        abort(400)


@api_view.route("/promotions/<int:promotion_id>/products/<uuid:product_id>",
                methods=["POST"], strict_slashes=False)
@jwt_required()
@is_admin
@swag_from(add_promotion_product_spec)
def add_promotion_product(promotion_id, product_id):
    """add a promotion to a product

    args:
        None
    Args:
        promotion_id (int): identifies the promotion by id
        product_id (str): uuid for a product
    Raises:
        401: unauthorised access to route
        400: bad request
        404: product or promotion not found
    Return:
        status, 200
    """
    promotion = storage.get("Promotion", int(promotion_id))
    if not promotion:
        raise InvalidApiUsage("promotion not found", status_code=404)
    product = storage.get("Product", str(product_id))
    if not product:
        raise InvalidApiUsage("product not found", status_code=404)
    promotion.products.append(product)
    storage.save()
    return {}, 200


@api_view.route("/promotions/<int:promotion_id>/products/<uuid:product_id>",
                methods=["DELETE"], strict_slashes=False)
@jwt_required()
@is_admin
@swag_from(delete_promotion_product_spec)
def delete_promotion_product(promotion_id, product_id):
    """Delete a promotion and product id from product_promotions table

    args:
        None
    Args:
        promotion_id (int): identifies the promotion to unlink
        product_id (str): identifies the product to unlink
    Raises:
        401: unauthorised access to route
        400: bad request
        404: product or promotion not found
    Return:
        No response
    """
    promotion = storage.get("Promotion", int(product_id))
    if not promotion:
        raise InvalidApiUsage("promotion not found", status_code=404)
    product = storage.get("Product", str(product_id))
    if not product:
        raise InvalidApiUsage("product not found", status_code=404)
    promotion.products.remove(product)
    storage.save()
    return {}, 204


@api_view.route("/promotions/<int:promotion_id>", methods=["PUT"], strict_slashes=True)
@jwt_required()
@is_admin
@isvalid("update_promotion_schema.json")
@swag_from(update_promotion_spec)
def update_promotion(promotion_id):
    """Update promotion if admin
    Args:
        promotion_id (int): identifies the promotion to delete
    args:
        None
    Raises:
        404: promotion not found
        401: unauthorised access to route
        400: bad request
    Response:
        new update promotions
    """
    promotion = storage.get("Promotion", int(promotion_id))
    if not promotion:
        raise InvalidApiUsage("promotion not found", status_code=404)
    body = request.get_json
    if body:
        promotion.update(**body)
    promotion.save()
    return promotion.to_dict()
