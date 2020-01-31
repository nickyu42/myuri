"""
Author: Nick Yu
Date Created: 7/31/2019

Pytest fixtures for session and db testing

Some parts used from
https://gist.github.com/alexmic/7857543 by Alex Michael
"""
import pytest
import tempfile
import os
from pathlib import Path
from typing import Optional
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from app import init_app
from app.config import TestingConfig
from app.database.models import db as _db
from app.data.base_parser import AbstractComicParser


@pytest.fixture(scope='session')
def app(request) -> Flask:
    """Session-wide test `Flask` application"""

    app = Flask(__name__)
    app.config.from_object(TestingConfig())

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app: Flask, request) -> SQLAlchemy:
    """Session-wide test database"""

    # for database access
    db_file, temp_path = tempfile.mkstemp(suffix='.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{temp_path}'

    # for comic image access
    fake_image, image_path = tempfile.mkstemp(suffix='jpeg')

    def teardown():
        _db.drop_all()
        os.close(db_file)
        os.close(fake_image)

    class MockComicParser(AbstractComicParser):
        """Mock the comic parser to always send a Path to a fake image file"""
        def get_volume_page(self, comic_id: int, volume: str, page: int) -> Optional[Path]:
            return Path(image_path)

        def get_page(self, comic_id: int, chapter: str, page: int) -> Optional[Path]:
            return Path(image_path)

        def get_cover(self, comic_id: int) -> Optional[Path]:
            return Path(image_path)

    init_app(app, MockComicParser(data_path=Path()))

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def db_session(db: SQLAlchemy, request) -> SQLAlchemy:
    """Creates a new database session for a test"""

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return db


@pytest.fixture(scope='function')
def client_db(db_session: SQLAlchemy) -> FlaskClient:
    """Test client with db session active"""

    with db_session.app.test_client() as client:
        client.db = db_session
        yield client


@pytest.fixture(scope='function')
def client(db: SQLAlchemy) -> FlaskClient:
    """Test client"""

    with db.app.test_client() as client:
        client.db = db
        yield client
