#!/usr/bin/env -S venv/bin/python3
"""Define chat_history model"""

from datetime import datetime

from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import (
    ForeignKey,
    Integer,
    Sequence,
    String,
    DateTime,
    Text,
    Column
)


class ChatHistory(BaseModel, Base):
    """Defines chat history model for db_storage"""
    __tablename__ = "chat_histories"
    id = Column(Integer, Sequence('chat_history_seq_id'), primary_key=True)
    user_id = Column(String(60), ForeignKey("users.id"))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.timestamp)
    customer = relationship(
        "ChatHistory", backref="chat_histories",
        cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """Initialized chathistory with basemodel __init__"""
        return super().__init__(*args, **kwargs)

    def to_dict(self):
        """Serialize chathistory"""
        new_dict = super().to_dict()
        if "customer" in new_dict:
            new_dict["customer"] = new_dict["customer"].to_dict()
        return new_dict
