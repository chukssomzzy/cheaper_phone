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
        "cart_products", uselist=False))

    @property
    def image(self):
        """Return product image"""
        if self.product:
            return self.product.image

    @property
    def name(self):
        """Returns product name"""
        if self.product:
            return self.product.name
        return ""

    @property
    def price(self):
        """Returns product price"""
        if self.product:
            return self.product.price
        return 0

    @property
    def total(self):
        """Get total price"""
        return self.quantity * self.price

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
        if new_dict.get("product"):
            new_dict["product"] = new_dict["product"].to_dict()
        return new_dict

    def augment_quantity(self, quantity):
        """Inc quantity by"""
        self.quantity = self.quantity + quantity
        self.save()
        return self.quantity
