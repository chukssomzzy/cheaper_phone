#!/usr/bin/env -S venv/bin/python3
"""Analytics Model"""


from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class Analytics(BaseModel, Base):
    """Defines analytics table"""
    __tablename__ = "analytics"
    id = Column(Integer, Sequence('analytics_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'))
    action = Column(String(50))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    customer = relationship(
        "Analytics", backref="analytics", cascade="all")

    def __init__(self, *args, **kwargs):
        """Initialize analytic model"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """Serialize analytics"""
        new_dict = super().to_dict()
        if "customer" in new_dict:
            new_dict["customer"] = new_dict["customer"].to_dict()
