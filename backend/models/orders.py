#!/usr/bin/env venv/bin/python3
"""Define order table for db_storage"""


import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, Numeric,
                        Sequence, String)
from sqlalchemy.orm import backref, relationship

from models.base_model import Base, BaseModel


class statusEnum(enum.Enum):
    """Defines Status Enum"""
    pending = "Pending"
    processing = "Processing"
    shipped = "Shipped"
    delivered = "Delivered"
    cancelled = "Cancelled"
    returned = "Returned"
    refunded = "Refunded"
    failed = "Failed"
    on_hold = "On Hold"
    ready_for_pickup = "Ready For Pickup"
    backordered = "Backordered"
    partial_shipment = "Partial Shipment"
    process_delayed = "Processing Delayed"
    payment_pending = "Payment Pending"
    payment_failed = "Payment Failed"


class Order(BaseModel, Base):
    """Defines order model"""
    __tablename__ = "orders"
    id = Column(Integer, Sequence('order_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    status = Column(Enum(statusEnum), default=statusEnum.pending)
    shipping_address_id = Column(Integer, ForeignKey("shipping_address.id"))
    items = relationship("OrderItem", backref="order")
    address = relationship(
        "ShippingAddress", backref=backref("order", uselist=False))
    customer = relationship("User", backref="orders")

    def __init__(self, *args, **kwargs):
        """Intialize order with __init__ from basemodel"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """serializable representation of obj"""
        new_dict = super().to_dict()
        if "status" in new_dict:
            new_dict["status"] = str(self.status.value)
        if "address" in new_dict:
            new_dict["address"] = new_dict["address"].to_dict()
        if "customer" in new_dict:
            new_dict["customer"] = new_dict["customer"].to_dict()
        if "address" in new_dict:
            new_dict["address"] = new_dict["address"].to_dict()
        return new_dict
