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
from models.order_items import OrderItem
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
                 "AdminLog": AdminLog, "Brand": Brand, "OrderItem": OrderItem}
    __engine = None

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
            self.session = self.__Session

    def delete(self, obj):
        """Delete a obj from session"""
        self.__Session.delete(obj)

    def new(self, obj):
        """Add a new obj to session"""
        self.__Session.add(obj)

    def save(self):
        """flush update in session to db"""
        self.__Session.commit()

    def all(self, cls=None, page=None, limit=None):
        """Return all object in db storage related to a cls or all obj"""
        allObj = {}
        for clss in self.__classes:
            if not cls or cls == clss or cls == self.__classes[clss]:
                for obj in self.__Session.query(self.__classes[clss]).all():
                    key = obj.__class__.__name__ + "." + str(obj.id)
                    allObj[key] = obj
                if cls and len(allObj):
                    return allObj
        return allObj

    def get(self, cls, id):
        """Return a cls related to an id"""
        if cls not in self.__classes and cls not in self.__classes.values():
            return None
        if cls in self.__classes:
            cls = self.__classes[cls]
        if self.__Session:
            return self.__Session.query(cls).\
                filter_by(id=id).one_or_none()

    def close(self):
        """Close the current session and request a new one"""
        if self.__Session:
            self.__Session.close()

    def count(self, cls):
        """Count rows in a specific class or all class"""
        obj_count = 0
        for clss in self.__classes:
            if not cls or cls is self.__classes[clss] or cls == clss:
                obj_count = self.__Session.query(self.__classes[clss]).count()
                if obj_count and cls:
                    return obj_count
        return obj_count

    def create(self, cls=None, **kwargs):
        """Takes a cls and accepts"""
        obj = {}
        if cls and cls in self.__classes:
            cls = self.__classes[cls]
            obj = cls(**kwargs)
            self.__Session.add(obj)
        elif cls and cls in self.__classes.values():
            obj = cls(**kwargs)
            self.__Session.add(obj)
        return (obj)

    def filter(self, cls, **kwargs):
        """Filter storage by list of kwargs"""
        obj_val = dict()
        if cls in self.__classes:
            cls = self.__classes[cls]
            filter_ses = self.__Session.query(cls)
            for key, val in kwargs.items():
                key_cls = getattr(cls, key)
                if key_cls:
                    filter_ses = filter_ses.filter(key_cls == val)
            for obj in filter_ses.all():
                key = obj.__class__.__name__ + "." + str(obj.id)
                obj_val[key] = obj
        return obj_val

    def exists(self, cls, id):
        """Check if an obj with a particular ID exists"""
        if cls and cls in self.__classes:
            cls = self.__classes[cls]
            return (self.__Session.query(cls).filter_by(id=id).exists())
        return (False)

    def page_all(self, cls="Product", page=1, limit=10, order_by="created_at"):
        """ Paginate all the data in the db based on the models class or
        paginate the product if cls is None
        Args:
            page: the page number of page we are currently on
            limit: the number of items to return per page
        Return:
            obj (dict->model_obj): return a dict of model or empty dict
        """
        obj = {}
        startIdx = 0
        endIdx = 0
        if cls in self.__classes:
            count = self.count(cls)
            if count > (page * limit):
                startIdx = (page - 1) * limit
                endIdx = page * limit
            else:
                startIdx = 0
                endIdx = count
            cls = self.__classes[cls]
            query = self.__Session.query(cls).order_by(
                getattr(cls, order_by))[startIdx:endIdx]
            for val in query:
                key = str(val.__class__.__name__) + "." + str(val.id)
                obj[key] = val
        return obj

    def page_join(self, cls, secCls, id, action="page", page=1, limit=10,
                  order_by="created_at"):
        """ Paginate a or count a joined models

        Args:
            cls: parent cls to paginate
            secCls: child class to join
            actions: to perform count or page
            page: if page what the current page
            limit: no of items per page
            order_by: key to order by
        Return:
            Count or dict
        """
        if cls not in self.__classes or secCls not in self.__classes:
            return None
        cls = self.__classes[cls]
        secCls = self.__classes[secCls]
        count = self.__Session.query(cls).join(
            getattr(cls, secCls.__name__)).filter(getattr(cls, "id") == id)\
            .count()
        endIdx = 0
        obj = {}

        if action == "count":
            return count
        endIdx = (page + 1) * limit if (page + 1) * limit < count else count
        startIdx = (page - 1) * limit if (page - 1) * limit < endIdx else 0
        if action == "page":
            for item in self.__Session.query(cls).join(getattr(cls, secCls))\
                    .filter(getattr(cls, "id") == id)\
                    .order_by(getattr(secCls, order_by))[startIdx:endIdx]:
                key = str(item.__class__.__name__) + "." + item.id
                obj[key] = item
        return obj
