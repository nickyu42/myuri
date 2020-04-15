"""
Author: Nick Yu
Date created: 23/7/2019
"""
import enum
import flask.json
from sqlalchemy.ext.declarative import declared_attr

from app.database import db


class BaseMixin:
    """Mixin class for extra base functionality"""

    def to_obj(self) -> dict:
        """
        Tries to guess all relevant fields and creates a dict from self
        :return: dict with all fields
        """
        if hasattr(self, 'serialization_fields'):
            params = self.serialization_fields
        else:
            # this also grabs tables
            params = [x for x in dir(self) if not x == 'id' and not x.startswith('_') and x != 'metadata']

        # deliberately ignores calling to_obj on attributes which are of type Model
        # this is done to prevent circular references from causing infinite recursive calls
        return {p: getattr(self, p) for p in params if hasattr(self, p)}

    def serialize(self) -> str:
        """
        Serializes the Model into a json bytes object
        Can optionally have a serialization_fields attribute to tell which fields to add
        :return: serialized model
        """
        return flask.json.dumps(self.to_obj(), default=str)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        columns = [f'{key}={val if len(str(val)) < 10 else "..."}' for key, val
                   in vars(self).items()
                   if not key.startswith('_')]
        return f'<{type(self).__name__} {" ".join(columns)}>'


class ComicDataMixin(BaseMixin):
    """Mixin class that that has a many to many relationship with Comic"""

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


class Chapter(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    number = db.Column(db.String, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)
    volume_id = db.Column(db.Integer, db.ForeignKey('volume.id'), nullable=True)

    def to_obj(self) -> dict:
        vol_nr = None

        if self.volume is not None:
            vol_nr = self.volume.number

        return flask.json.dumps({
            'title': self.title,
            'number': self.number,
            'total_pages': self.total_pages,
            'comic': self.comic,
            'volume_number': vol_nr
        }, default=str)


class Volume(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=True)

    chapters = db.relationship('Chapter', lazy=True, backref=db.backref('volume', lazy=True))

    serialization_fields = ['number']


class ComicName(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)

    serialization_fields = ['name']


class Tag(ComicDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String)

    serialization_fields = ['val']


class Artist(ComicDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String)


class Author(ComicDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String)


class Genre(ComicDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String)


class Comic(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    serialization_fields = [
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
