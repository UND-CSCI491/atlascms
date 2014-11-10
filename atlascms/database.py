from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    uri = current_app.config['SQLALCHEMY_DATABASE_URI']
except:
    from atlascms.configs import ConfigDevelopment
    uri = ConfigDevelopment.SQLALCHEMY_DATABASE_URI

# setup our engine and session
engine = create_engine(uri)
db_session = sessionmaker(
        autocommit=False,
#        autoflush=False,
        bind=engine)
session = db_session()

# create a base model
Base = declarative_base()
Base.metadata.bind = engine
