#!/usr/bin/env venv/bin/python3
"""Define brand for each product"""

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class Brand(BaseModel, Base):
    """Define Brands Table """
    __tablename__ = 'brands'
    id = Column(Integer, Sequence('brand_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    products = relationship("Product", backref="brand",
                            cascade="delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize brands table"""
        return super().__init__(*args, **kwargs)
