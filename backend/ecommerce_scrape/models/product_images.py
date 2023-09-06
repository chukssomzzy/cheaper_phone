#!/usr/bin/env -S venv/bin/python3

"""product_images table"""


from sqlalchemy import ForeignKey, Integer, String, Column
from models.base_model import Base, BaseModel


class ProductImage(BaseModel, Base):
    """Product image and metadata column"""
    __tablename__ = "product_images"
    image_url = Column(String(200), nullable=False, unique=True)
    caption = Column(String(200))
    alt_text = Column(String(200))
    order = Column(Integer)
    product_id = Column(String(60), ForeignKey("products.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        """product_images table"""
        return super().__init__(*args, **kwargs)