"""mysql configuration file"""
import os
from . import config


class Config(object):
    """mysql configuration to app"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # ...
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + config.MYSQL_USER_ID + ":" +\
                              config.MYSQL_PASSWORD + "@" + config.MYSQL_HOST + "/" + config.MYSQL_DATABASE \
                              + "?host=" + config.MYSQL_HOST + "?port=3306"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 10