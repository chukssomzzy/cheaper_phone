#!/usr/bin/env -S venv/bin/python3

"""admin_log table"""


from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from models.base_model import Base, BaseModel


class AdminLog(BaseModel, Base):
    """Defines admin_log"""
    __tablename__ = "adminlogs"
    id = Column(Integer, Sequence('adminlog_seq_id'), primary_key=True)
    admin_id = Column(String(60))
    action = Column(String(100))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize adminlog"""
        return super().__init__(*args, **kwargs)
