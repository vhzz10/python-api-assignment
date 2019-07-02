# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from faker import Faker
import random


Base = declarative_base()

class Customer(Base):

    __tablename__ = 'customer'

    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String)
    dob = Column(Date)
    updated_at = Column(DateTime(timezone=True),
                            default=func.now(),
                            onupdate=func.now())

    def __repr__(self):
        return "<Customer(name='%s', dob='%s')>" % (self.name, self.dob)

    def to_dict(self):
        intersection = set(self.__table__.columns.keys()) & set(self.FIELDS)
        return dict(
            map(
                lambda key: (
                    key,
                    (lambda value: self.FIELDS[key](value) if value else None)(
                        getattr(self, key)
                    ),
                ),
                intersection,
            )
        )

    FIELDS = {"name": str, "dob": str}

    @classmethod
    def get_id(cls):
        return Customer.id

    @classmethod
    def find_one(cls, session, id):
        return session.query(cls).filter(cls.get_id() == id).one()

    @classmethod
    def find_update(cls, session, id, data):
        session.query(cls).filter(cls.get_id() == id).update(data)
        return session.query(cls).filter(cls.get_id() == id).one()






