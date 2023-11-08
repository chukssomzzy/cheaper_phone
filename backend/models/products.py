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
    stripe_products_id = Column(String(100), unique=True)

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
        if new_dict.get("reviews"):
            reviews_list = []
            for review in new_dict["reviews"]:
                reviews_list.append(review.to_dict())
            new_dict["reviews"] = reviews_list
        if new_dict.get("images"):
            images_list = []
            for image in new_dict["images"]:
                images_list.append(image.to_dict())
            new_dict["images"] = images_list
        if new_dict.get("categories"):
            categories_list = []
            for category in new_dict["categories"]:
                categories_list.append(category.to_dict())
            new_dict["categories"] = categories_list

        if new_dict.get("brand"):
            new_dict["brand"] = new_dict["brand"].to_dict()

        if new_dict.get("comments"):
            comments_list = []
            for comment in new_dict["comments"]:
                comments_list.append(comment.to_dict())
            new_dict["comments"] = comments_list
        if new_dict.get("promotions"):
            promotions_list = []
            for promotion in new_dict["promotions"]:
                promotions_list.append(promotion.to_dict())
            new_dict["promotions"] = promotions_list
        if new_dict.get("cart_product"):
            new_dict["cart_product"] = new_dict["cart_product"].to_dict()
        return new_dict
