#!/usr/bin/env -S venv/bin/python3
"""Defines Category table"""


from sqlalchemy import Sequence, Column, String, Integer
from models.base_model import BaseModel, Base


class Category(BaseModel, Base):
    """Defines Category table for db_storage"""
    __tablename__ = "categories"
    id = Column(Integer, Sequence('category_seq_id'), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        """Initializd category model with basemodel __init__"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """use the inherited to_dict to serialize"""
        new_dict = super().to_dict()
        if "products" in "new_dict":
            for product in new_dict["products"]:
                new_dict["products"].append(product.to_dict())
            return new_dict
