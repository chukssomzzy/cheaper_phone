from flasgger import swag_from
from api.v1.views import api_view
from models import storage
from api.v1.views.documentation.index import status_specs, stats_specs

"""Defines api to get status and stats"""


@api_view.route("/status", strict_slashes=False)
@swag_from(status_specs)
def get_api_status():
    """Returns the api status
    Args:
        None
    Response:
        status: "OK"
    """
    return {"status": "OK"}


@api_view.route("/stats")
@swag_from(stats_specs)
def get_api_stats():
    """Return number rows in each public table in
    the database
    Response:
        brands (int): count of rows in the brands table
        categories (int): count of rows in the category table
        product (int): count of rows in  the product table
        promotions (int): count of rows in the promotion table
        customers (int): count of rows in the users table
        """
    classes = {"Brand": "brands", "Category": "categories",
               "Product": "products", "User": 'customers'}
    stat_obj = {}
    for cls, val in classes.items():
        stat_obj[val] = storage.count(cls)
    return stat_obj
