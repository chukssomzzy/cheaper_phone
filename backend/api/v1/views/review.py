#!/usr/bin/env venv/bin/python3
"""review endpoint"""
from flask import abort, request, url_for
from flask_jwt_extended import jwt_required
from sqlalchemy.sql.functions import current_user
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from models import storage


@api_view.route("/review/user/<uuid:user_id>/products/<uuid:product_id>",
                strict_slashes=False)
def get_product_review(user_id, product_id):
    """Get a review for a particular product

        Args
            user_id (str): uuid for user
            product_id (str): uuid for product
        args
            None
        Response
            dict representation of review
        Raise:
            404: review does not exits
    """
    reviews = storage.filter(
        "ProductReview", user_id=user_id, product_id=product_id)
    if not reviews:
        raise InvalidApiUsage(
            f"no review for product {product_id} by user {user_id}",
            status_code=404)
    reviews_list = []
    for review in reviews.values():
        reviews_list.append(review.to_dict())
    reviews_dict = {}
    reviews_dict["reviews"] = reviews_list
    return reviews_dict


@api_view.route("customer/review/products/<uuid:product_id>", methods=["POST"],
                strict_slashes=False)
@jwt_required()
@isvalid("review_schema.json")
def post_product(product_id):
    """post a product review
    Args
        product_id (int): product uuid
    args
        None
    Response
        dict representation of new review
    Raises
        400 bad request
        401 unauthorized access
        404 product doesn't exit
    """
    customer = current_user
    product = storage.get("Product", id=str(product_id))

    if not product:
        raise InvalidApiUsage("product not found", status_code=404)
    review = request.get_json()
    review["user_id"] = customer.id
    review["product_id"] = str(product_id)
    review = storage.create("ProductReview", **review)
    if not review:
        abort(400)
    storage.save()
    review_dict = review.to_dict()
    review_dict["id"] = review.id
    return review_dict, 201


@api_view.route("customer/review/products/<uuid:product_id>",
                strict_slashes=False)
def get_all_review(product_id):
    """Get all review for a product and take it average
    Args:
        product_id (uuid): uuid for product
    args:
        None
    Response:
        dict response of the review
    Raises:
        404: product not found
        400: bad request
    """
    product = storage.get("Product", id=product_id)
    if not product:
        abort(404)
    reviews = product.reviews
    reviews_dict = []
    for review in reviews:
        review_dict = review.to_dict()
        review_dict["user"] = review.user.to_dict()
        review_dict["user"]["role"] = str(review.user.role)
        if review_dict.get("product"):
            del review_dict["product"]
        reviews_dict.append(review_dict)
    rating = product.rating
    review = {"rating": rating, "reviews": reviews_dict}
    return review


@api_view.route("customer/review/<int:review_id>",
                methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_review(review_id):
    """Delete a review
    Args:
        product_id (uuid) for product
    args:
        None
    Response:
        no response with 204 status code
    Raises:
        404: product doesn't exit
        401: unauthorized access
        400: bad request
    """
    customer = current_user
    review = storage.filter(
        "ProductReview", user_id=customer.id, id=review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 204
