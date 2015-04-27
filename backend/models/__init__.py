import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime

from backend import db


class Entity(object):
	id = Column(Integer, primary_key=True)
	created_on = Column(DateTime, default=datetime.datetime.now)


# All the models
from sessions import Session
from users import User
