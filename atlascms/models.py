from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, CheckConstraint, or_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import BINARY
from atlascms.database import Base
import datetime

class User(Base):
    '''User information.'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email       = Column(String(128), unique=True)
    username    = Column(String(32), unique=True)
    password    = Column(BINARY(60), nullable=False)
    name        = Column(String(64))
    phone       = Column(String(11))

    def __init__(self, email, username, password, name=None, phone=None):
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone
