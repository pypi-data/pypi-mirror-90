"""
Core Objects and Connections for Access in Sickdb Models
"""

import hiredis  # force this dependency for performance
import redis
from flask import Response
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, MetaData
from flask_sqlalchemy import SQLAlchemy

import dada_settings
from dada_types import T
from dada_utils import path
from dada_stor import DadaStor

from dada_errors import RequestError

# /////////
# API Database Connection
# /////////
db = SQLAlchemy()

# s3 connection
s3conn = DadaStor()

# ma<-> sql alchemy schema engine
ma = Marshmallow()

# redis cache connection
rdsconn = redis.from_url(
    dada_settings.REDIS_CACHE_URL,
    db=dada_settings.REDIS_CACHE_DB,
    **dada_settings.REDIS_CACHE_KWARGS,
)

# For running other queries not in the app context.
DB_ENGINE = create_engine(dada_settings.SQLALCHEMY_DATABASE_URI)
DB_META = MetaData(bind=DB_ENGINE, reflect=True)


def db_execute(query: T.sql.py):
    """
    Execute a query against the database outside of the appplication context.
    :yield dict
    """
    try:
        with DB_ENGINE.connect() as connection:
            result = connection.execute(query)
            if result.returns_rows:
                return (dict(row.items()) for row in result)
            else:
                return True
    except Exception as e:
        raise RequestError(f"{e}")
