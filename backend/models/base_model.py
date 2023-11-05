#!venv/bin/python3

"""Defines base model """
import copy
from datetime import datetime
from uuid import uuid4

import models
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()


class BaseModel():
    """Basemodel that would define common attribute that would be shared by
    all model"""
    id = Column(String(60), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialized the model if kwargs is present"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of model"""
        return "[%s.%s](%r)" % (
            self.__class__.__name__, self.id, self.to_dict()
        )

    def save(self):
        """Save the current model to database"""
        self.update_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Delete this model from storage"""
        models.storage.delete(self)

    def update(self, *args, **kwargs):
        """update kwargs"""
        not_key = ["id", "created_at", "updated_at"]
        for key, val in kwargs.items():
            if key not in not_key:
                setattr(self, key, val)

    def to_dict(self):
        """Return a dictionary representation of the current object"""
        new_dict = copy.deepcopy(self.__dict__)
        if "created_at" in new_dict:
            new_dict['created_at'] = datetime.isoformat(new_dict["created_at"])
        if "updated_at" in new_dict:
            new_dict["updated_at"] = datetime.isoformat(new_dict["updated_at"])
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        new_dict["__class__"] = self.__class__.__name__
        return new_dict
