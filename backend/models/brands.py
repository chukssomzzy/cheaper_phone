#!/usr/bin/env venv/bin/python3
"""Define brand for each product"""

from sqlalchemy import Column, Integer, Sequence, String
from models.base_model import Base, BaseModel


class Brand(BaseModel, Base):
    """Define Brands Table """
    __tablename__ = 'brands'
    id = Column(Integer, Sequence('brand_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize brands table"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """serialize brand"""
        new_dict = super().to_dict()
        if new_dict.get("products"):
            product_list = []
            for product in new_dict["products"]:
                product_list.append(product.to_dict())
            new_dict["products"] = product_list
        return new_dict
