#!/usr/bin/python3
"""This is the state class"""
import os
from models.base_model import BaseModel
from models.city import City
from models.base_model import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="states", cascade="delete")
    else:
        @property
        def cities(self):
            """FileStorage relationship between State and City """
            cities = models.storage.all(City)
            cities_relation = []
            for city in cities.values():
                if city.state_id == self.id:
                    cities_relation.append(city)
            return cities_relation
