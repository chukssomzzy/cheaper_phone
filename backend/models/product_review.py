#!/usr/bin/env -S venv/bin/python3

"""product review model"""


from sqlalchemy import ForeignKey, Integer, Sequence, Column, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class ProductReview(BaseModel, Base):
    """Product review table"""
    __tablename__ = "product_reviews"
    id = Column(Integer, Sequence('product_review_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey("users.id"))
    product_id = Column(String(60), ForeignKey("products.id"))
    rating = Column(Integer)
    customer = relationship(
        "User", backref="reviews",
        cascade="all, delete")
    product = relationship("Product",
                           backref="reviews", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """Initialize product review table"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """serialize while using inherited to_dict"""
        new_dict = super().to_dict()
        if new_dict.get("product"):
            new_dict["product"] = new_dict["product"].to_dict()
        if new_dict.get("customer"):
            new_dict["customer"] = new_dict["customer"].to_dict()
        return new_dict
