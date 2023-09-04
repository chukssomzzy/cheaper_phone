#!/usr/bin/env -S venv/bin/python3
"""Analytics Model"""


from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String
from models.base_model import Base, BaseModel


class Analytics(BaseModel, Base):
    """Defines analytics table"""
    __tablename__ = "analytics"
    id = Column(Integer, Sequence('analytics_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'))
    action = Column(String(50))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize analytic model"""
        return super().__init__(*args, **kwargs)
