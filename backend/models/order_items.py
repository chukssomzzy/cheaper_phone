#!/usr/bin/env -S venv/bin/python3
"""Order_items model """

from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class OrderItem(BaseModel, Base):
    """Define order_items model"""
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(String(60), ForeignKey(
        "products.id"), primary_key=True)
    product = relationship("Product")

    def __init__(self, *args, **kwargs):
        """Initialized order_items"""
        return super().__init__(*args, **kwargs)
