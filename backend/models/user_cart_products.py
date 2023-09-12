#!/usr/bin/env -S venv/bin/python3
"""Defines association table for products and user_cart"""


from sqlalchemy import Column, ForeignKey, Integer, String
from models.base_model import BaseModel, Base


class UserCartProducts(BaseModel, Base):
    """Defines column for foreignKey between the product and user_cart"""
    id = None
    user_cart_id = Column(Integer, ForeignKey(
        "user_cart.id"), primary_key=True)
    product_id = Column(String(60), ForeignKey(
        "products.id"), primary_key=True)
    quantity = Column(Integer, default=0)
    cart = relationship("UserCart", backref="cart_products")
    product = relationship("P")
