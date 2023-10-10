#!/usr/bin/env venv/bin/python3
"""comments endpoints"""
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from models import storage
from models.comments import Comment
from models.products import Product


@api_view.route("/reviews/products/<uuid:product_id>/comments",
                strict_slashes=False)
def get_comments(product_id):
    """Returns all comment made on a product

    Args:
        product_id (str): uuid for product
    args:
        limit (int): maximum comments to return per page
        page (int): page number we are current on
        order_by (str): what to sort comments by
    Response:
        dictionary representation of comments
    Raises:
        400: bad request
        404: product does not exit
    """
    try:
        product = storage.get("Product", str(product_id))

        if not product:
            InvalidApiUsage(
                f"product with product_id {product_id} not found",
                status_code=404)
        limit = int(request.args.get("limit", 10))
        page = int(request.args.get("page", 1))
        order_by = request.args.get("order_by", "created_by")
        order_bys = ['created_by', 'updated_by', 'id', 'content']
        if order_by not in order_bys:
            order_by = "created_by"

        comment_count = storage.session.query(Product).join(
            Product.comments).filter_by(id=product_id).count()
        comment_count = int(comment_count)
        comment_count = int(comment_count / limit)
        comments_list = []
        for comment in storage.page_join("Product", "Comment",
                                         product_id, limit=limit,
                                         order_by=order_by).values():
            comment_dict = comment.to_dict()
            comment_dict["user"] = comment.user.to_dict()
            comments_list.append(comment_dict)
        comments_dict = {}
        comments_dict["comments"] = comments_list
        comments_dict["pagination"] = {
            "page": page, "limit": limit, "pages": comment_count}
        comments_dict["actions"] = []
        comments_dict["actions"].append({"order_by": order_bys})
        return comments_dict
    except TypeError:
        raise InvalidApiUsage("Wrong type to args")


@api_view.route("customer/reviews/products/<uuid:product_id>/comments",
                methods=["POST"], strict_slashes=False)
@isvalid("comment_schema.json")
@jwt_required()
def post_comment(product_id):
    """post a comment for a product

    Args:
        product_id (str): uuid for a product
    args:
        None
    Response:
        dict representation of a comment
    Raises:
        400: bad request
        404: product doesn't exist
        401: unauthorized access
        500: server error
    """
    product = storage.get("Product", id=product_id)
    if not product:
        raise InvalidApiUsage("product not found", status_code=404)
    comment_body = request.get_json()
    comment = Comment(**comment_body)
    if not comment:
        InvalidApiUsage(
            f"Couldn't create comment for product {product_id}",
            status_code=500)
    storage.save()
    comment_dict = comment.to_dict()
    comment_dict["id"] = comment.id
    return comment_dict


@api_view.route("customer/reviews/product/<uuid:product_id>/comments",
                methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_commment(product_id):
    """ Delete a comment

    Args:
        product_id (str): uuid for a product
    args:
        None
    Response:
        no content with status code 204
    Raises:
        400: bad request
        404: product doesn't exist
        401: unauthorized access to route
        500: server error
    """
    product = storage.get("Product", id=product_id)
    if not product:
        raise InvalidApiUsage("Product not found", status_code=404)
    return {}, 204
