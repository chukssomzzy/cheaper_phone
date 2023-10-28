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

    brand = relationship("Brand", backref="products",
                         cascade="delete")
    categories = relationship(
        "Category", secondary=product_category, backref='products',
        cascade="delete")

    def __init__(self, *args, **kwargs):
        """Intialized product table with basemodel __init__"""
        return super().__init__(*args, **kwargs)

    @property
    def rating(self):
        """Return average rating for a product"""
        if self.reviews:
            rating = [review.rating for review in self.reviews]
            rating = sum(rating) / len(rating)
        else:
            rating = 0
        return rating

    @property
    def image(self):
        """Return product first image"""
        if self.images:
            return self.images[0]

    def to_dict(self):
        """serialize related object"""
        new_dict = super().to_dict()
        if "reviews" in new_dict:
            for review in new_dict["reviews"]:
                new_dict["reviews"].append(review.to_dict())
        if "images" in new_dict:
            for image in new_dict["images"]:
                new_dict["images"].append(image.to_dict())
        if "categories" in new_dict:
            for category in new_dict["categories"]:
                new_dict["categories"].append(category.to_dict())
        if "brand" in new_dict:
            new_dict["brand"] = new_dict["brand"].to_dict()

        if "comments" in new_dict:
            for comment in new_dict["comments"]:
                new_dict["comments"].append(comment.to_dict())
        if "promotions" in new_dict:
            for promotion in new_dict["promotions"]:
                new_dict["promotions"].append(promotion.to_dict())
        if "cart_product" in new_dict:
            for promotion in new_dict["promotions"]:
                new_dict["cart_product"] = new_dict["cart_product"].to_dict()
        return new_dict
