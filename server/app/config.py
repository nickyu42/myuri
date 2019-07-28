"""
Author: Nick Yu
Date created: 23/7/2019
"""
import os


class Config:
    """Default config variables"""

    # TODO change absolute path to environment variable
    _path = os.path.realpath(os.getcwd() + '/data')
    _db_name = os.environ.get('DB_NAME', default='db')

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{_path}/{_db_name}.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Config for production environment"""
    pass


class DevelopmentConfig(Config):
    """Config for development environment"""
    DEBUG = True

