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
        if new_dict.get("customer"):
            new_dict["customer"] = new_dict["customer"].to_dict()
        if new_dict.get("items"):
            item_list = []
            for item in new_dict["items"]:
                item_list.append(item.to_dict())
            new_dict["items"] = item_list
        return new_dict

    @property
    def items_no(self):
        """Return number of items in cart"""
        if self.items:
            return len(self.items)
        return 0

    @property
    def total_items(self):
        """Return subtotal"""
        total = 0
        if self.items:
            total = sum(item.price * item.quantity for item in self.items)
        return total
