#!/usr/bin/env -S venv/bin/python3
"""user_cart model for db_storage"""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from models.base_model import BaseModel, Base


class UserCart(BaseModel, Base):
    """ DEfines usercart for in db_storage"""
    __tablename__ = "user_cart"
    user_id = Column(String(60), ForeignKey("users.id"))
    items = relationship("UserCartProduct")
    customer = relationship("User", backref=backref(
        "cart", uselist=False), cascade="delete")

    def __init__(self, *args, **kwargs):
        """Initialized usercart with __init__ defined in basemodel"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """serialize usercart"""
        new_dict = super().to_dict()
        if "customer" in new_dict:
            new_dict["customer"] = new_dict["customer"].to_dict()
        if "items" in new_dict:
            for item in new_dict["items"]:
                new_dict["items"].append(item.to_dict())
        return new_dict
