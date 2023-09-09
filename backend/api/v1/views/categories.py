#!/usr/bin/env -S venv/bin/python3
"""endpoints for categories"""
from flask import abort, request, url_for
from sqlalchemy.exc import IntegrityError
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view

from models import storage
from models.categories import Category


@api_view.route("/categories", strict_slashes=False)
def get_categories():
    """Get all categories in the db
    Args:
        None
    arg:
        limit (int): maximum number of category to return
        page (int): current page to return from
        order_by (str): string key to order property by
    Response:
        dict: categories dict representation
        pagination: pagination information for categories
        order_by: list contain args response could be order by
    Raises
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        order_by = str(request.args.get("order_by"))
        order = ["created_at", "name", "price", "update_at"]
        if order_by not in order:
            order_by = "created_at"
        categories = []
        for category in storage.page_all("Category", limit=limit, page=page,
                                         order_by=order_by).values():
            category_dict = category.to_dict()
            category_dict["actions"] = [{"fetch_related_product": url_for(
                ".get_category_products", _external=True,
                category_id=category.id)}]
            categories.append(category_dict)
        count = storage.count("Category")
        no_pages = int(count / limit)

    except TypeError:
        raise InvalidApiUsage("wrong args types")
    return {"paginate": {"page": page, "limit": limit, "pages": no_pages},
            "products": categories, "actions":
            {"order_by": order}}


@api_view.route("/category/<int:category_id>/products", strict_slashes=False)
def get_category_products(category_id):
    """Get product by category
    Args:
        category_id (int): id for category
    args:
        limit (int): maximum item per page
        page (int): number of page to get from db
        order_by (str): key to order the item by
    Raises:
        400 : bad request from client
        404: no products found for the category
    Response:
        dict: containing the product and category with information about
        pagination and actions
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        order_by = str(request.args.get("order_by"))
        order = ["created_at", "name", "price", "update_at"]
        if order_by not in order:
            order_by = "created_at"
        category = storage.get("Category", category_id)
        if not category:
            abort(404)
        products = []
        count = storage.session.query(Category).join(
            Category.products).filter(Category.id == category.id).count()
        pages = int(count / limit)
        endIdx = page * limit if (page * limit) < count else count
        startIdx = (page - 1) * limit if (page - 1) * limit < endIdx else 0
        for product in category.products[startIdx:endIdx]:
            product_dict = product.to_dict()
            if product_dict.get("images"):
                del product_dict["images"]
                product_dict["image"] = product.images[0]
            product_dict["url_key"] = url_for(".get_products", _external=True)
            products.append(product_dict)
        res_dict = {}
        res_dict["category"] = category.to_dict()
        if res_dict["category"].get("products"):
            del res_dict["category"]["products"]
        res_dict["category"]["products"] = products
        res_dict["pagination"] = {"page": page, "limit": limit, "pages": pages}
        res_dict["actions"] = {"order_by": order}
        return res_dict
    except TypeError:
        raise InvalidApiUsage("your args are not correct")


@api_view.route("/category", methods=["POST"], strict_slashes=False)
@isvalid("category_schema.json")
def post_category():
    """Post to a category if category user is admin
    Args:
        None
    args:
        None
    Response:
        Category : return the newly created category
    Raises:
        401: if user is not authorised to create a category
        400: bad request from user
    """
    try:
        body = request.get_json()
        category = storage.create("Category", **body)
        storage.save()
        if not category:
            raise InvalidApiUsage("Couldn't get category after save")
        category_dict = {"category": category.id}
        return (category_dict), 201

    except IntegrityError:
        storage.session.rollback()
        raise InvalidApiUsage("Category already exist")


@api_view.route("/category/<int:category_id>", methods=["DELETE"],
                strict_slashes=False)
def delete_category(category_id):
    """Delete a category from database
    Args:
        category_id (int): unique identifier for product
    args:
        None
    Response:
        No content
        status_code: 204
    Raises:
        400 bad request
        401 unauthorised access
    """
    category = storage.get("Category", category_id)
    if not category:
        raise InvalidApiUsage(
            f"category_id {category_id} does not identify a category")
    storage.delete(category)
    storage.save()
    return {}, 204
