#!/usr/bin/env -S venv/bin/python3
"""Product comments table"""


from sqlalchemy import Column, ForeignKey, Text
from models.base_model import Base, BaseModel


class Comment(BaseModel, Base):
    """defines Comment table for products"""
    __tablename__ = "comments"
    user_id = Column("User", ForeignKey('users.id'), nullable=False)
    product_id = Column("Product", ForeignKey('products.id'), nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize comment table"""
        return super().__init__(*args, **kwargs)
