#!/usr/bin/env -S venv/bin/python3

"""Model for users table """

import enum
import hashlib
import secrets

from sqlalchemy import Column, Enum, String

from models.base_model import Base, BaseModel
from flask_login import UserMixin


class RoleEnum(enum.Enum):
    """Defines users roles"""
    customer = "customer"
    admin = "admin"


class User(BaseModel, Base, UserMixin):
    """Defines users table for db storage"""
    __tablename__ = "users"
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    _pwd_hash = Column(String(128), nullable=False, server_default="")
    email = Column(String(50), unique=True)
    _salt = Column(String(32), nullable=False, server_default="")
    role = Column(Enum(RoleEnum),
                  nullable=False, server_default="customer")
    stripe_customer_id = Column(String(50), nullable=False)
    phone = Column(String(20))

    def __init__(self, *args, **kwargs):
        """Pass kwargs to basemodel for parsing"""
        return super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Returns password hash for the current user"""
        raise AttributeError("No attribute password")

    @password.setter
    def password(self, new_pwd):
        """Takes a password and generate a salt and password hash for the
        user
        """
        salt = secrets.token_hex(16)
        salted_pwd = salt + new_pwd
        hashed_pwd = hashlib.sha256(salted_pwd.encode()).hexdigest()
        self._salt = salt
        self._pwd_hash = hashed_pwd

    def check_password(self, password):
        """Recreate the password and check if it the equal to the one stored
           the db
        """
        salted_pwd = self._salt + password
        hashed_pwd = hashlib.sha256(salted_pwd.encode()).hexdigest()
        return self._pwd_hash == hashed_pwd

    def get_default_address(self):
        """ get default address for the current user"""
        for address in self.addresses:
            if address.default:
                return address
        return None

    def to_dict(self):
        """dictionary representation of object"""
        new_dict = super().to_dict()
        if "role" in new_dict:
            new_dict["role"] = str(self.role.value)
        if "reviews" in new_dict:
            for review in new_dict["reviews"]:
                new_dict["reviews"].append(review.to_dict())
        if "chat_histories" in new_dict:
            for chat_history in new_dict["chat_histories"]:
                new_dict["chat_histories"].append(chat_history.to_dict())
        if 'analytics' in new_dict:
            for analytics in new_dict["analytics"]:
                new_dict["analytics"].append(analytics.to_dict())
        if "orders" in new_dict:
            for order in new_dict["orders"]:
                new_dict["orders"].apppend(order.to_dict())
        if "cart" in new_dict:
            new_dict["cart"] = new_dict["cart"].to_dict()
        return new_dict

    def get_id(self):
        """Returns userid"""
        return str(self.id)
