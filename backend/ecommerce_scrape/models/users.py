#!/usr/bin/env -S venv/bin/python3

"""Model for users table """

from sqlalchemy import Column, String
from sqlalchemy.orm import backref, relationship
from models.base_model import Base
from models.base_model import BaseModel


class User(BaseModel, Base):
    """Defines users table for db storage"""
    __tablename__ = "users"
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(50))
    email = Column(String(50), unique=True)
    cart = relationship("UserCart", backref=backref(
        "user", userList=False), cascade="delete")
    shipping_address = relationship(
        "ShippingAddress", order_by="shipping_address.id", backref="user",
        cascade="delete, delete-orphan")
    reviews = relationship(
        "ProductReview", order_by="product_reviews.id", backref="user",
        cascade="delete, delete-orphan")
    orders = relationship("Order", order_by="orders.id",
                          backref="user", cascade="delete, delete-orphan")
    chat_history = relationship(
        "ChatHistory", order_by="chat_histories.id", backref="user",
        cascade="delete, delete-orphan")
    analytics = relationship(
        "Analytics", order_by="analytics.id", backref="user")

    def __init__(self, *args, **kwargs):
        """Pass kwargs to basemodel for parsing"""
        return super().__init__(*args, **kwargs)
