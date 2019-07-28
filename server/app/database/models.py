"""
Author: Nick Yu
Date created: 23/7/2019
"""
import enum
from typing import Type

from app.database.db import db


class BaseMixin:
    """Mixin class for extra functionality"""

    @staticmethod
    def _create(cls: Type[db.Model], *args, **kwargs):
        obj = cls(*args, **kwargs)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an instance of this Model"""
        cls._create(cls, *args, **kwargs)

    def __repr__(self: db.Model):
        return f'<{type(self).__name__}>'


class KeyMixin(BaseMixin):
    """Mixin class with primary key set by default"""
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        columns = [f'{key}={val}' for key, val in vars(self).items() if not key.startswith('_')]
        return f'<{type(self).__name__} {" ".join(columns)}>'


class ComicType(enum.Enum):
    """Enum for comic types"""
    Japanese = 1
    Korean = 2
    Chinese = 3
    Western = 4


class Comic(KeyMixin, db.Model):
    type = db.Column(db.Enum(ComicType), nullable=False)
    total_chapters = db.Column(db.Integer, nullable=True)
    total_volumes = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)


class Chapter(KeyMixin, db.Model):
    total_pages = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)


class ComicName(KeyMixin, db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)


def create_data_class(name: str) -> Type:
    """
    Creates a metaclass that represents a table
    with a many-to-many relationship with Comic
    :param name: name to give the table
    :return: Class object
    """
    return type(
        name,
        (KeyMixin, db.Model),
        {
            '__tablename__': name,
            'val': db.Column(db.String(80), unique=True, nullable=False),
            'comic_id': db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False),
            'table': db.Table(
                f'{name}_comic',
                db.Column(f'{name}_id', db.Integer, db.ForeignKey(f'{name}.id'), primary_key=True),
                db.Column('comic_id', db.Integer, db.ForeignKey('comic.id'), primary_key=True)
            )
        }
    )


Tag = create_data_class('tag')
Artist = create_data_class('artist')
Author = create_data_class('author')
Genre = create_data_class('genre')


