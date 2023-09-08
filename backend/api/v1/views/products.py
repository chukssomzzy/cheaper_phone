#!/usr/bin/env -S venv/bin/python3

"""Api view for products"""

from flask import abort, request, url_for
from api.v1.utils.schemas.is_valid import isvalid
from api.v1.views import api_view
from api.v1.utils.error_handles.invalid_api_error import InvalidApiUsage
from models import storage


@api_view.route("/products", strict_slashes=False)
def get_prducts():
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
                                        page=int(page), order_by=order_by).values():
            product_dict = product.to_dict()
            if product.brand:
                product_dict["brand"] = product.brand.to_dict()
            del product_dict["brand_id"]
            if product.categories:
                product_dict["categories"] = []
                for category in product.categories:
                    product_dict["categories"].append(category.to_dict())
            if product.images:
                image_url = product.images[0]
                product_dict["image_url"] = image_url.to_dict().get(
                    "image_url")
                product_dict["url_key"] = url_for(
                    ".get_product_by_id",
                    product_id=product.id, _external=True)
            products.append(product_dict)
        if not products:
            abort(404, "Products table is empty")
        no_pages = int(count / limit)
    except TypeError:
        raise InvalidApiUsage("wrong args types")
    return {"paginate": {"page": page, "limit": limit, "pages": no_pages},
            "products": products, "actions": {"order_by": order}}


@api_view.route('/products/<uuid:product_id>', strict_slashes=False)
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
        abort(404)
    product_return = product.to_dict()
    del product_return["brand_id"]
    if product.brand:
        product_return["brand"] = product.brand.to_dict()
    product_return["categories"] = []
    for category in product.categories:
        product_return["categories"].append(category.to_dict())
    product_return["images"] = []
    for image in product.images:
        product_return['images'].append(image.image_url)
    return product_return


@api_view.route("/product_id", methods=["POST"], strict_slashes=False)
@isvalid("products_schema")
def post_products()
