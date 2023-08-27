#!/usr/bin/env -S venv/bin/python3

"""product review model"""


from sqlalchemy import ForeignKey, Integer, Sequence, Column, String
from models.base_model import Base, BaseModel


class ProductReview(BaseModel, Base):
    """Product review table"""
    __tablename__ = "product_reviews"
    id = Column(Integer, Sequence('product_review_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey("users.id"))
    product_id = Column(String(60), ForeignKey("products.id"))
    rating = Column(Integer)

    def __init__(self, *args, **kwargs):
        """Initialize product review table"""
        return super().__init__(*args, **kwargs)
