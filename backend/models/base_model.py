#!venv/bin/python3

"""Defines base model """
from datetime import datetime
from sqlalchemy import DateTime, Column, String
from sqlalchemy.orm import declarative_base

import uuid

import models


Base = declarative_base()


class BaseModel():
    """Basemodel that would define common attribute that would be shared by
    all model"""
    id = Column(String(128), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialized the model if kwargs is present"""
        if kwargs:
            for key, val in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at' and \
                            type(key) == str:
                        setattr(self, key, datetime.utcfromtimestamp(val))
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.update_at = self.created_at

    def __repr__(self):
        """String representation of model"""
        return "[%s.%s](%r)" % (
            self.__class__.__name__, self.id, self.to_dict()
        )

    def save(self):
        """Save the current model to database"""
        self.update_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def deletes(self):
        """Delete this model from storage"""
        models.storage.delete(self)

    def update(self, *args, **kwargs):
        """update kwargs"""
        for key, val in kwargs.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(self, key, val)

    def to_dict(self):
        """Return a dictionary representation of the current object"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict['created_at'] = datetime.isoformat(new_dict["created_at"])
        if "updated_at" in new_dict:
            new_dict["updated_at"] = datetime.isoformat(new_dict["updated_at"])
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        new_dict["__class__"] = self.__class__.__name__
        return new_dict
