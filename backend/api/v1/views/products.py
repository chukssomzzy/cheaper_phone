from flask import abort, request
from api.v1.views import api_view
from api.v1.utils.invalid_api_error import InvalidApiUsage
from models import storage

"""Api view for products"""


@api_view.route("/products", strict_slashes=False)
def get_prducts():
    """Get all product data and pages the product to a limit of 40 by default
    args:
        page (int): product page to return
        limit (int): amount to limit the page by
    response:
        products: array of products
        paginate: (dict) contains pagination information
        actions: contains action that can be performed on a product
    raises:
        NotFound: If no product was found in the db
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        products = []
        count = storage.count("Product")
        for product in storage.page_all("Product", limit=int(limit),
                                        page=int(page)).values():
            products.append(product.to_dict())
        if not products:
            abort(404, "Products table is empty")
        no_pages = int(count / limit)
    except TypeError:
        raise InvalidApiUsage("wrong args types")
    return {"paginate": {"page": page, "limit": limit, "pages": no_pages},
            "products": products}
