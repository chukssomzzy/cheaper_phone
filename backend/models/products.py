#!/usr/bin/env -S venv/bin/python3
"""Defines product class for db storage"""


from collections import UserList
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import backref, relationship
from models.base_model import BaseModel, Base


product_category = Table("product_categories", Base.metadata,
                         Column("product_id", ForeignKey(
                             "products.id"), primary_key=True),
                         Column("category_id", ForeignKey("categories.id"),
                                primary_key=True))


class Product(BaseModel, Base):
    """Defines table and relationship for product table"""
    __tablename__ = "products"
    id = Column(String(60), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    product_images = Column(
        String(200), ForeignKey("product_images.image_url"))
    images = relationship("ProductImage", order_by="product_images.order",
                          backref="product", cascade="delete, delete-orphan")
    reviews = relationship("ProductReview", order_by="product_reviews.id",
                           backref="product", cascade="delete, delete-orphan")
    categories = relationship(
        "Category", secondary=product_category, backref='products',
        cascade="delete")

    def __init__(self, *args, **kwargs):
        """Intialized product table with basemodel __init__"""
        return super().__init__(*args, **kwargs)
