"""
Author: Nick Yu
Date created: 23/7/2019
"""
import enum

from app.database.db import db


class Chapter(db.Model):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True)
    total_pages = db.Column(db.Integer, nullable=False)

    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)
    comic = db.relationship('Comic', backref=db.backref('chapters', lazy=True))

    def __repr__(self):
        return f'<Chapter {self.id}>'


class ComicType(enum.Enum):
    Manga = 1
    Manhwa = 2
    Manhua = 3
    Western = 4


class Comic(db.Model):
    __tablename__ = 'comic'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(ComicType), nullable=False)
    author = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Comic {self.id}>'


class ComicName(db.Model):
    __tablename__ = 'comicname'

    id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return f'<ComicName {self.name}>'

