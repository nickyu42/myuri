"""
Author: Nick Yu
Date created: 23/7/2019
"""
import enum
import flask.json
from typing import Type
from sqlalchemy.ext.declarative import declared_attr

from app.database.db import db


class BaseMixin:
    """Mixin class for extra base functionality"""

    @staticmethod
    def _create(cls: Type[db.Model], *args, **kwargs):
        obj = cls(*args, **kwargs)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an instance of this Model"""
        cls._create(cls, *args, **kwargs)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self: db.Model):
        return f'<{type(self).__name__}>'


class KeyMixin(BaseMixin):
    """Mixin class with primary key set by default"""
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        columns = [f'{key}={val if len(str(val)) < 10 else "..."}' for key, val
                   in vars(self).items()
                   if not key.startswith('_')]
        return f'<{type(self).__name__} {" ".join(columns)}>'


class ComicDataMixin(KeyMixin):
    """Mixin class that that has a many to many relationship with Comic"""
    val = db.Column(db.String(80), unique=True, nullable=False)

    @declared_attr
    def comic_id(cls):
        return db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)

    @declared_attr
    def table(cls):
        name = cls.__tablename__
        return db.Table(
            f'{name}_comic',
            db.Column(f'{name}_id', db.Integer, db.ForeignKey(f'{name}.id'), primary_key=True),
            db.Column('comic_id', db.Integer, db.ForeignKey('comic.id'), primary_key=True)
        )


class ComicType(enum.Enum):
    """Enum for comic types"""
    Japanese = 1
    Korean = 2
    Chinese = 3
    Western = 4


class ComicFormat(enum.Enum):
    """Enum for comic formats"""
    LeftToRight = 1
    RightToLeft = 2
    Webtoon = 3


class Chapter(KeyMixin, db.Model):
    number = db.Column(db.Integer, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)
    volume_id = db.Column(db.Integer, db.ForeignKey('volume.id'), nullable=True)


class Volume(KeyMixin, db.Model):
    number = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)

    chapters = db.relationship('Chapter', lazy=True, backref=db.backref('Volume', lazy=True))


class ComicName(KeyMixin, db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)


class Tag(ComicDataMixin, db.Model):
    """Comic tag table"""


class Artist(ComicDataMixin, db.Model):
    """Comic artist table"""


class Author(ComicDataMixin, db.Model):
    """Comic author table"""


class Genre(ComicDataMixin, db.Model):
    """Comic genre table"""


class Comic(KeyMixin, db.Model):
    type = db.Column(db.Enum(ComicType), nullable=True)
    total_chapters = db.Column(db.Integer, nullable=True)
    total_volumes = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    format = db.Column(db.Enum(ComicFormat), nullable=True)

    names = db.relationship('ComicName', lazy='joined', backref=db.backref('comic', lazy='joined'))

    # a comic is loaded without chapters/volume
    # while in reverse direction the loading is joined because
    # usually the chapter/volume is required with the corresponding Comic metadata
    chapters = db.relationship('Chapter', lazy=True, backref=db.backref('comic', lazy='joined'))
    volumes = db.relationship('Volume', lazy=True, backref=db.backref('comic', lazy='joined'))

    # metadata is loaded as necessary
    # chapters are usually filtered based on metadata, so subquery is used
    tags = db.relationship('Tag', lazy=True, secondary=Tag.table, backref=db.backref('comics', lazy='dynamic'))
    artists = db.relationship('Artist', lazy=True, secondary=Artist.table, backref=db.backref('comics', lazy='dynamic'))
    authors = db.relationship('Author', lazy=True, secondary=Author.table, backref=db.backref('comics', lazy='dynamic'))
    genres = db.relationship('Genre', lazy=True, secondary=Genre.table, backref=db.backref('comics', lazy='dynamic'))

    @property
    def json(self):
        params = [
            'type',
            'total_chapters',
            'total_volumes',
            'description',
            'format',
            'names',
            'tags',
            'artists',
            'authors',
            'genres'
        ]

        return flask.json.dumps({p: getattr(self, p) for p in params}, default=str)
