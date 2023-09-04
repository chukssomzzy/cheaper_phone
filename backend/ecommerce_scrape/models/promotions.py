#!/usr/bin/env -S venv/bin/python3

"""promotions table model"""


from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String
from models.base_model import Base, BaseModel


class Promotion(BaseModel, Base):
    """Defines promotions table"""
    __tablename__ = "promotions"
    id = Column(Integer, Sequence('promotional_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.timestamp)

    def __init__(self, *args, **kwargs):
        """Initialize promotions table"""
        return super().__init__(*args, **kwargs)
