#!/usr/bin/env -S venv/bin/python3
"""user_cart model for db_storage"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class UserCart(BaseModel, Base):
    """ DEfines usercart for in db_storage"""
    __tablename__ = "user_cart"
    user_id = Column(String(60), ForeignKey("users.id"))
    items = relationship("Product", backref="cart")

    def __init__(self, *args, **kwargs):
        """Initialized usercart with __init__ defined in basemodel"""
        return super().__init__(*args, **kwargs)
