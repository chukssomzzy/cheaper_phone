#!/usr/bin/env -S venv/bin/python3

"""promotions table model"""

import datetime

from models.base_model import Base, BaseModel
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Sequence,
                        String, Table)

product_promotions = Table("product_promotions", Base.metadata,
                           Column("product_id", String(60),
                                  ForeignKey("products.id"), primary_key=True),
                           Column("promotion_id", String(60),
                                  ForeignKey("promotions.id"), primary_key=True)
                           )
# changes
# -
# user_id = Column(String(60), ForeignKey('users.id'))
# action = Column(String(50), nullable=False)
# timestamp = Column(DateTime, nullable=False, default=datetime.timestamp)
#
# +
# name = Column(String(100), nullable=False)
# discount = Column(Integer, nullable=False)
# duration = Column(DateTime, nullable=False, default=datetime.timedelta(days=30))
# start_date = Column(DateTime, nullable=False, default=datetime.datetime.now())


class Promotion(BaseModel, Base):
    """Defines promotions table"""
    __tablename__ = "promotions"
    id = Column(Integer, Sequence('promotional_seq_id'), primary_key=True)
    name = Column(String(100), nullable=False)
    discount = Column(Integer, nullable=False)
    duration = Column(DateTime, nullable=False,
                      default=datetime.timedelta(days=30))
    start_date = Column(DateTime, nullable=False,
                        default=datetime.datetime.now())

    def __init__(self, *args, **kwargs):
        """Initialize promotions table"""
        if "duration" in kwargs:
            kwargs["duration"] = self.parse_delta(kwargs["duration"])
        return super().__init__(*args, **kwargs)

    def is_expired(self):
        """Check if a promotion has expired"""
        duration_date = self.start_date + self.duration
        return (datetime.datetime.now()) > duration_date

    def to_dict(self):
        """serializes duration"""
        new_dict = super().to_dict()
        if "duration" in new_dict:
            new_dict["duration"] = str(new_dict["duration"])
        if "discount" in new_dict:
            new_dict["discount"] = str(new_dict["discount"]) + "%"
        return new_dict

    def parse_delta(self, delta):
        """Parse delta"""
        if type(delta) != str:
            raise TypeError("must be a str")
        days = int(delta.split(",")[0].strip() or 0)
        time_part = delta.split(",")[1]
        if not time_part:
            raise TypeError("not a timedelta str")
        hours = int(time_part.split(":")[0].strip())
        if not hours:
            raise TypeError("not a timedelta str")
        minutes = int(time_part.split(":")[1].strip())
        if not minutes:
            raise TypeError("not a timedelta str")
        seconds = int(time_part.split(":")[2].strip())
        if not seconds:
            raise TypeError("not a timedelta str")
        microseconds = int(time_part.split(".")[1].strip()) or 0
        return datetime.timedelta(days=days, hours=hours, minutes=minutes,
                                  seconds=seconds, microseconds=microseconds)
