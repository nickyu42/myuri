"""
Author: Nick Yu
Date created: 23/7/2019
"""
from flask import Blueprint
from app.database.db import db
from app.database.models import Chapter

db_routes = Blueprint('db_routes', __name__)


@db_routes.route('/db/create')
def create():
    db.create_all()
    return 'created'


@db_routes.route('/db/chapters')
def chapters():
    return '\n'.join(map(str, Chapter.query.all()))
