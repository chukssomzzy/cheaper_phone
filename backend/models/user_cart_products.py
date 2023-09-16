#!/usr/bin/env -S venv/bin/python3
"""Defines association table for products and user_cart"""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from models.base_model import BaseModel, Base


class UserCartProduct(BaseModel, Base):
    """Defines column for foreignKey between the product and user_cart"""
    __tablename__ = "user_cart_products"
    id = None
    user_cart_id = Column(Integer, ForeignKey(
        "user_cart.id"), primary_key=True)
    product_id = Column(String(60), ForeignKey(
        "products.id"), primary_key=True)
    quantity = Column(Integer, default=0)
    products = relationship("Product")
