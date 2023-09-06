#!/usr/bin/env -S venv/bin/python3
"""Defines product class for db storage"""


from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text
)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


product_category = Table("product_categories", Base.metadata,
                         Column("product_id", ForeignKey(
                             "products.id"), primary_key=True),
                         Column("category_id", ForeignKey("categories.id"),
                                primary_key=True))


class Product(BaseModel, Base):
    """Defines table and relationship for product table"""
    __tablename__ = "products"
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    images = relationship("ProductImage",
                          backref="product", cascade="all, delete")
    reviews = relationship("ProductReview",
                           backref="product", cascade="all, delete")
    categories = relationship(
        "Category", secondary=product_category, backref='products',
        cascade="delete")

    def __init__(self, *args, **kwargs):
        """Intialized product table with basemodel __init__"""
        return super().__init__(*args, **kwargs)
