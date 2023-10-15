#!/usr/bin/env -S venv/bin/python3

"""Api view for products"""

from flasgger import swag_from
from flask import abort, request, url_for
from flask_jwt_extended import current_user, jwt_required
from models import storage
from models.base_model import BaseModel

from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from api.v1.utils.jwt.is_admin import is_admin
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from api.v1.views.documentation.products import (get_product_by_id_spec,
                                                 get_products_spec,
                                                 post_product_spec,
                                                 update_product_spec,
                                                 delete_product_spec)

# add to cart
# remove from cart
# reduce quantity of an item in cart


@api_view.route("/products", strict_slashes=False)
@jwt_required(optional=True)
@swag_from(get_products_spec)
def get_products():
    """Get all product data and pages the product to a limit of 40 by default
    Request_args:
        page (int): product page to return
        limit (int): amount to limit the page by
        order_by (str): order result by a value
    response:
        products: dicts of product containing information related to the
        product
        paginate: (dict) contains pagination information
        actions: contains action that can be performed on a product
    raises:
        NotFound: Not found
        TypeError: wrong request args
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        order_by = str(request.args.get("order_by"))
        order = ["created_at", "name", "price", "update_at"]
        if order_by not in order:
            order_by = "created_at"
        products = []
        count = storage.count("Product")
        for product in storage.page_all("Product", limit=int(limit),
                                        page=int(page), order_by=order_by)\
                .values():
            product_dict = {}
            product_dict["data"] = product.to_dict()
            if product.brand:
                product_dict["brand"] = product.brand.to_dict()
            del product_dict["data"]["brand_id"]
            if product.categories:
                product_dict["categories"] = []
                for category in product.categories:
                    product_dict["categories"].append(category.to_dict())
            if product.images:
                image_url = product.images[0]
                product_dict["data"]["image_url"] = image_url.to_dict().get(
                    "image_url")
                product_dict["data"]["url_key"] = url_for(
                    ".get_product_by_id",
                    product_id=product.id, _external=True)

            product_dict["actions"] = []
            if current_user:
                product_dict["actions"].append({"add_to_cart": url_for(
                    ".add_product_to_cart", product_id=product.id,
                    _external=True), "methods": ["GET"]})
                product_dict["actions"].append({"remove_from_cart": url_for(
                    ".remove_product_from_cart", product_id=product.id, _external=True
                ), "methods": ["PUT"]})
                product_dict["actions"].append({"delete_from_cart": url_for(
                    ".delete_from_cart", product_id=product.id, _external=True
                ), "methods": ["DELETE"]})
            product_dict["actions"].append({"get_product_by_id": url_for(
                ".get_product_by_id", product_id=product.id, _external=True),
                "methods": ["GET"]})

            products.append(product_dict)
        if not products:
            abort(404, "Products table is empty")
        no_pages = int(count / limit)
    except TypeError:
        raise InvalidApiUsage("wrong args types")
    return {"pagination": {"page": page, "limit": limit, "pages": no_pages},
            "products": products, "actions": {"order_by": order}}


@api_view.route('/products/<uuid:product_id>', strict_slashes=False)
@jwt_required(optional=True)
@swag_from(get_product_by_id_spec)
def get_product_by_id(product_id):
    """Get a product by an id

    args:
        product_id (uuid:str): identifies the uuid to query to query
    response:
        id: unque identify of the products
        reviews: current reviews for the product if any
        comment: text review for the product
        images: array of images for the product
        description: description for the specific product
        brand: brand information for the product
        categories: array of category information for the product
        actions: action that can be done on the specific product
    raise:
        NotFound: Not found
    """
    product_return = {}
    product = storage.get("Product", str(product_id))
    if not product:
        abort(404, "product not found")
    product_return = {}
    product_return["data"] = product.to_dict()
    del product_return["brand_id"]
    if product.brand:
        product_return["brand"] = product.brand.to_dict()
    product_return["categories"] = []
    for category in product.categories:
        product_return["categories"].append(category.to_dict())
    product_return["images"] = []
    for image in product.images:
        product_return["data"]['images'].append(image.image_url)
    if current_user:
        product_return["actions"] = []
        product_return["actions"].append({"add_to_cart": url_for(
            ".add_product_to_cart", product_id=product.id, _external=True),
            "methods": ["POST"]})
        product_return["actions"].append({"remove_from_cart": url_for(
            ".remove_product_from_cart", product_id=product.id, _external=True
        ), "methods": ["PUT"]})
        product_return["actions"].append({"delete_from_cart": url_for(
            ".delete_from_cart", product_id=product.id, _external=True
        ), "methods": ["DELETE"]})
    return product_return


@api_view.route("/products", methods=["POST"], strict_slashes=False)
@isvalid("products_schema.json")
@jwt_required()
@is_admin
@swag_from(post_product_spec)
def post_products():
    """Post a product to the database
    Response:
        product_dict: json_dict of a product
    Raises:
        400 bad request
        401 unauthorized user
    """
    body = request.get_json()
    product = storage.create("Product", **body)
    if not isinstance(product, BaseModel):
        InvalidApiUsage("Product Not Created")
    storage.save()
    return {"product": str(product.id)}, 201


@api_view.route("/products/<uuid:product_id>", methods=["PUT"],
                strict_slashes=False)
@isvalid("product_update_schema.json")
@jwt_required()
@is_admin
@swag_from(update_product_spec)
def update_product(product_id):
    """update a product
    Args:
        product_id: unique identifier for a product
    body:
        what to update (name, price, brand, description)
    "
    Response:
        product: dict
    Raises:
        404: if product not in database
        400: wrong format for product
        401: unauthorized user
    """
    product = storage.get("Product",  str(product_id))
    if not product:
        abort(404, "product doesn't exits")
    body = request.get_json()
    product.update(**body)
    product.save()
    return product.to_dict()


@api_view.route("/products/<uuid:product_id>",
                methods=['DELETE'], strict_slashes=False)
@jwt_required()
@is_admin
@swag_from(delete_product_spec)
def delete_product(product_id):
    """Delete a product from the database
    Args:
        product_id: uuid for the product
    args:
        no args
    Response:
        no content
    Raises:
        404: products doesn't exits
        401: unauthorized access
    """
    products = storage.get("Product", str(product_id))
    if not products:
        abort(404, "Product not found")
    storage.delete(products)
    storage.save()
    return {}, 204
