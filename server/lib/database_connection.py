from contextlib import contextmanager

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import URL

import os
from dotenv import load_dotenv


@contextmanager
def db_session():

    """ Creates a context with an open SQLAlchemy session.
    """
    url = URL.create(
        drivername="postgresql",
        host= os.getenv('DATABASE_HOST'),
        database=  os.getenv('DATABASE_NAME')
    )
    engine = create_engine(url)
    """
    Create a new _engine.Engine instance.
    The standard calling form is to send the URL <database_urls> as the first positional argument, 
    usually a string that indicates database dialect and connection arguments:
    engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
    """
    connection = engine.connect()
    meta = MetaData()
    meta.reflect(bind=engine)
    Base = declarative_base()

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield db_session
    db_session.commit()
    db_session.close()
    connection.close()
