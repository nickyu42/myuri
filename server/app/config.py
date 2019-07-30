"""
Author: Nick Yu
Date created: 23/7/2019
"""
import os
from pathlib import Path


class Config:
    """Default config variables"""

    _db_name = os.environ.get('DB_NAME', default='db.sqlite')
    _data_folder = os.environ.get('DATA_FOLDER', default='./data')
    _path = Path(_data_folder).resolve()

    DEBUG = False
    TESTING = False

    # TODO make path generation more secure
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{_path}/{_db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Config for production environment"""
    pass


class DevelopmentConfig(Config):
    """Config for development environment"""
    DEBUG = True


class TestingConfig(Config):
    """Config for running unit tests"""
    SQLALCHEMY_DATABASE_URI = 'sqlite//'
    TESTING = True
