# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from faker import Faker
from datetime import datetime
import random

from app import config
from app.models import Customer

fake = Faker()

def get_engine(uri):
    options = {
        "pool_recycle": 3600,
        "pool_size": 10,
        "pool_timeout": 30,
        "max_overflow": 30,
    }
    return create_engine(uri, **options)


db_session = scoped_session(sessionmaker())

if not database_exists(config.DATABASE_URL):
    create_database(config.DATABASE_URL)

engine = get_engine(config.DATABASE_URL)


def init_session():
    db_session.configure(bind=engine)

    from app.models import Base

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def gen_dob():
        cur_time = datetime.now()
        return datetime(random.randrange(1911,cur_time.year), random.randrange(1, 12), random.randrange(1, 28))

    for i in range(0, 10):
        db_session.add_all([Customer(name=fake.name(), dob=gen_dob())])
        db_session.commit()