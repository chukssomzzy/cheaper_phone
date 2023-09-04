#!/usr/bin/env -S venv/bin/python3
"""Defines db_storage"""


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.admin_logs import AdminLog
from models.analytics import Analytics
from models.base_model import Base
from models.categories import Category
from models.chat_history import ChatHistory
from models.comments import Comment
from models.orders import Order
from models.product_images import ProductImage
from models.product_review import ProductReview
from models.products import Product
from models.promotions import Promotion
from models.shipping_address import ShippingAddress
from models.user_cart import UserCart
from models.users import User
from models.brands import Brand
from os import getenv


class DBStorage:
    """Storage interface for database"""
    __classes = {"User": User, "UserCart": UserCart,
                 "ShippingAddress": ShippingAddress, "Promotion": Promotion,
                 "Product": Product, "ProductReview": ProductReview,
                 "ProductImage": ProductImage, "Order": Order,
                 "Comment": Comment, "ChatHistory": ChatHistory,
                 "Category": Category, "Analytics": Analytics,
                 "AdminLog": AdminLog, "Brand": Brand}
    __engine = None
    __session = None

    def __init__(self):
        """Connects sqlalchemy to storage and creates an engine"""
        db_name = getenv("ECOMMERCE_DB")
        db_user = getenv("ECOMMERCE_USER")
        db_password = getenv("ECOMMERCE_PWD")
        db_host = getenv("ECOMMERCE_HOST")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".
            format(db_user, db_password, db_host, db_name))
        if getenv("ECOMMERCE_ENV") != "DEV":
            Base.metadata.dropall(self.__engine)

    def reload(self):
        """Reload and allocate a scoped session"""
        if self.__engine:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine)
            Session = scoped_session(session_factory)
            self.__Session = Session
            self.session = self.__Session()

    def delete(self, obj):
        """Delete a obj from session"""
        self.session.delete(obj)

    def new(self, obj):
        """Add a new obj to session"""
        self.session.add(obj)

    def save(self):
        """flush update in session to db"""
        self.session.commit()

    def all(self, cls=None):
        """Return all object in db storage related to a cls or all obj"""
        allObj = {}
        for clss in self.__classes:
            if not cls or cls == clss or cls == self.__classes[clss]:
                for obj in self.session.query(self.__classes[clss]).all():
                    key = obj.__class__.__name__ + "." + obj.id
                    allObj[key] = obj
                if cls and len(allObj):
                    return allObj
        return allObj

    def get(self, cls, id, pk="id"):
        """Return a cls related to an id"""
        if cls not in self.__classes or cls in self.__classes.values():
            return None
        else:
            if cls in self.__classes:
                cls = self.__classes[cls]
            if self.__session:
                return self.__session.query(cls).filter(cls[pk] == id)

    def close(self):
        """Close the current session and request a new one"""
        if self.__session:
            self.__session.remove()

    def count(self, cls):
        """Count rows in a specific class or all class"""
        obj_count = 0
        for clss in self.__classes:
            if not cls or cls is self.__classes[clss] or cls == clss:
                obj_count = self.session.query(self.__classes[clss]).count()
                if obj_count and cls:
                    return obj_count
        return obj_count

    def create(self, cls=None, **kwargs):
        """Takes a cls and accepts"""
        obj = {}
        if cls and cls in self.__classes:
            cls = self.__classes[cls]
            obj = cls(**kwargs)
            self.session.add(obj)
        elif cls and cls.get("__name__") in self.__classes:
            obj = cls(**kwargs)
            self.session.add(obj)
        else:
            return obj

    def exists(self, cls, id):
        """Check if an obj with a particular ID exists"""
        if cls and cls in self.__classes:
            cls = self.__classes[cls]
            return (self.session.query(cls).filter_by(id=id).exists())
        return (False)
