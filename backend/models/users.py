#!/usr/bin/env -S venv/bin/python3

"""Model for users table """

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import backref, relationship
from models.base_model import Base
from models.base_model import BaseModel


class User(BaseModel, Base):
    """Defines users table for db storage"""
    __tablename__ = "users"
    id = Column(String(60), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(50))
    email = Column(String(50), unique=True)
    cart = relationship("UserCart", backref=backref(
        "user", uselist=False), cascade="delete")
    shipping_address = relationship(
        "ShippingAddress", backref="user",
        cascade="all, delete")
    reviews = relationship(
        "ProductReview", backref="user",
        cascade="all, delete")
    orders = relationship("Order",
                          backref="user", cascade="all, delete")
    chat_history = relationship(
        "ChatHistory", backref="user",
        cascade="all, delete")
    analytics = relationship(
        "Analytics", backref="user", cascade="all")

    def __init__(self, *args, **kwargs):
        """Pass kwargs to basemodel for parsing"""
        return super().__init__(*args, **kwargs)
