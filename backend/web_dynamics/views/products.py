#!/usr/bin/env -S venv/bin/python3
"""Defines product endpoints"""
from os import getenv
from flask import render_template, session
from models import storage
from models.products import Product

from web_dynamics.views import web_dynamics

api_url = getenv("ECOMMERCE_API_URL")


@web_dynamics.route("/product/<uuid:product_id>", methods=["GET"],
                    strict_slashes=False)
def get_product_detail(product_id):
    """Render product details"""
    print(session.__dict__)
    product = storage.get("Product", str(product_id))
    reviews = storage.page_join("Product", "Review", id=str(product_id))
    reviews_count = storage.sec_count("Product", "Review", id=str(product_id))
    brand = product.brand
    related_products = storage.session.query(Product).filter(
        Product.name.like('%{}%'.format(product.name[10])))[:10]
    latest_products = storage.page_all(order_by="created_at")
    comments = storage.page_join("Product", "Comment", id=str(product_id))
    return render_template("pages/product.html",
                           product=product, reviews=reviews,
                           reviews_count=reviews_count, brand=brand,
                           related_products=related_products,
                           latest_products=latest_products,
                           comments=comments, api_url=api_url)
