#!/usr/bin/env -S venv/bin/python3

"""promotions table model"""

import datetime

from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, Sequence,
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

time = "%Y-%m-%dT%H:%M:%S.%f"


class Promotion(BaseModel, Base):
    """Defines promotions table"""
    __tablename__ = "promotions"
    id = Column(Integer, Sequence('promotional_seq_id'), primary_key=True)
    name = Column(String(100), nullable=False)
    discount = Column(Integer, nullable=False)
    duration = Column(String(50), nullable=False,
                      default=str(datetime.timedelta(days=30)))
    start_date = Column(DateTime, nullable=False,
                        default=datetime.datetime.now())
    isexpired = Column(Boolean, nullable=False, default=False)
    products = relationship(
        "Product", secondary=product_promotions, backref="promotions")

    def __init__(self, *args, **kwargs):
        """Initialize promotions table"""
        if "start_date" in kwargs and type(kwargs["start_date"]) is str:
            kwargs["start_date"] = datetime.datetime.strptime(
                kwargs["start_date"], time)
        return super().__init__(*args, **kwargs)

    def is_expired(self):
        """Check if a promotion has expired"""
        duration_date = self.start_date + self.parse_delta(self.duration)
        return (datetime.datetime.now()) > duration_date

    def to_dict(self):
        """serializes duration"""
        new_dict = super().to_dict()
        if new_dict.get("duration"):
            new_dict["duration"] = str(new_dict["duration"])
        if new_dict.get("discount"):
            new_dict["discount"] = str(new_dict["discount"]) + "%"
        if new_dict.get("products"):
            products_dict = []
            for product in new_dict["products"]:
                products_dict.append(product.to_dict())
            new_dict["products"] = products_dict
        return new_dict

    def parse_delta(self, delta):
        """Parse delta"""
        if type(delta) is str:
            raise TypeError("must be a str")
        days = delta.split(",")[0].strip() or 0
        days = int(str(days).split()[0])
        time_part = delta.split(",")[1]
        if not time_part:
            raise TypeError("time not a timedelta str")
        hours = time_part.split(":")[0].strip()
        if not hours:
            raise TypeError("no hours in str")
        hours = int(hours)
        minutes = time_part.split(":")[1].strip()
        if not minutes:
            raise TypeError("no minutes in str")
        minutes = int(minutes)
        seconds = time_part.split(":")[2].strip()
        if not seconds:
            raise TypeError("no sec in str")
        seconds = int(seconds)
        microseconds = 0
        if len(time_part.split(".")) == 2:
            microseconds = int(time_part.split(".")[1].strip()) or 0
        time_delta_r = datetime.timedelta(days=days, hours=hours, minutes=minutes,
                                          seconds=seconds, microseconds=microseconds)
        return time_delta_r
