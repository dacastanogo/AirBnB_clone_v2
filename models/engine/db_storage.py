#!/usr/bin/python3
""" Database Storage Engine """

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy as db


class DBStorage:
    """
    This class is the database storage engine
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize an instance
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query all objects from the current db session, based on class name
        """
        my_list = ["State", "City", "User", "Place", "Review", "Amenity"]
        dictio = {}
        if cls is None:
            for table in my_list:
                query = self.__session.query(eval(table)).all()
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dictio[key] = obj
        else:
            query = self.__session.query(eval(cls)).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dictio[key] = obj
        return dictio

    def new(self, obj):
        """
        add the object to the current databse session
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        commit changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete obj from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """Thread specific storage"""
        self.__session.close()
