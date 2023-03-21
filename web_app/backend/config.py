"""
    config.py
    - settings for the flask application object
"""

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False