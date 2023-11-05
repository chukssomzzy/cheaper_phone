#!/usr/bin/env -S venv/bin/python3

"""product_images table"""


from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class ProductImage(BaseModel, Base):
    """Product image and metadata column"""
    __tablename__ = "product_images"
    image_url = Column(String(200), nullable=False, unique=True)
    caption = Column(String(200))
    alt_text = Column(String(200))
    order = Column(Integer)
    product_id = Column(String(60), ForeignKey("products.id"), nullable=False)
    product = relationship("Product",
                           backref="images", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """product_images table"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """serialize productImage while using inherited to_dict"""
        new_dict = super().to_dict()
        if new_dict.get("product"):
            new_dict["product"] = new_dict["product"].to_dict()
        return new_dict
