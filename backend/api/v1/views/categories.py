#!/usr/bin/env -S venv/bin/python3
"""endpoints for categories"""
from flask import request
from api.v1.views import api_view


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
