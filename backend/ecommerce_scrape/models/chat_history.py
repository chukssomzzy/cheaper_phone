#!/usr/bin/env -S venv/bin/python3
"""Define chat_history model"""

from datetime import datetime
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

    def __init__(self, *args, **kwargs):
        """Initialized chathistory with basemodel __init__"""
        return super().__init__(*args, **kwargs)
