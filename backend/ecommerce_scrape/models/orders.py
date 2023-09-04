#!/usr/bin/env venv/bin/python3
"""Define order table for db_storage"""


from datetime import datetime
import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Numeric, Sequence, String, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


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
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    status = Column(Enum(statusEnum), default=statusEnum.pending)
    shipping_address_id = Column(Integer, ForeignKey("shipping_address.id"))
    items = relationship("OrderItem", backref="order")
    address = relationship(
        "ShippingAddress", order_by="shipping_address.id")

    def __init__(self, *args, **kwargs):
        """Intialize order with __init__ from basemodel"""
        return self().__init__(*args, **kwargs)
