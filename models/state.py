#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import models
from models.city import City


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City",
                          cascade="all, delete",
                          backref="_state")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """returns list of City instances with state_id"""
            from models import storage
            from models import City
            return [value for key, value in storage.all(City).items()
                    if value.state_id == self.id]
