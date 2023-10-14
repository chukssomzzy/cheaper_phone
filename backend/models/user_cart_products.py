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
    quantity = Column(Integer, default=1)
    product = relationship("Product", backref=backref(
        "cart_product", uselist=False))

    def increase_quantity(self):
        """increase the quantity of a product"""
        self.quantity = self.quantity + 1

    def decrease_quantity(self):
        """Decrease quantity of a product"""
        if int(self.quantity) > 1:
            self.quantity = self.quantity - 1
        else:
            self.delete()

    def to_dict(self):
        """update user cart product serializer"""
        new_dict = super().to_dict()
        if "product" in new_dict:
            new_dict["product"] = new_dict["product"].to_dict()
        return new_dict
