#!/usr/bin/env venv/bin/activate
"""shipping_address model"""

import enum
from sqlalchemy import Boolean, Enum, ForeignKey, Sequence, Column, Integer, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class AddressTypeEnum(enum.Enum):
    """Address type enum"""
    residential = 'Residential'
    commercial = 'Commercial'
    others = 'others'


class ShippingAddress(BaseModel, Base):
    """Define shipping address for model"""
    __tablename__ = "shipping_address"
    id = Column(Integer, Sequence('shipping_address_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey("users.id"))
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    address_type = Column(Enum(AddressTypeEnum),
                          nullable=False, default=AddressTypeEnum.residential)
    orders = relationship("Order", backref="address", cascade="all")

    def __init__(self, *args, **kwargs):
        """Initialize shipping address"""
        return super().__init__(self, *args, **kwargs)
