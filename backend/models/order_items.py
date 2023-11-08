#!/usr/bin/env -S venv/bin/python3
"""Order_items model """

from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class OrderItem(BaseModel, Base):
    """Define order_items model"""
    __tablename__ = "order_items"
    id = None
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(String(60), ForeignKey(
        "products.id"), primary_key=True)
    product = relationship("Product")

    order = relationship("Order", backref="items")

    def __init__(self, *args, **kwargs):
        """Initialized order_items"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """serialize orderItem"""
        new_dict = super().to_dict()
        if new_dict.get("product"):
            new_dict["product"] = new_dict["product"].to_dict()
        return new_dict
