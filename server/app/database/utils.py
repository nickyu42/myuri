"""
Author: Nick Yu
Date created: 23/7/2019
"""
import click
from flask.cli import AppGroup

from app.database.models import *

db_cli = AppGroup('db')


@db_cli.command('create')
def create():
    """Creates tables"""
    db.create_all()
    print('[db] created tables')


@db_cli.command('view')
@click.argument('table')
def view(table: str):
    """
    Prints given objects in 'table'
    :param table: name of the table to view
    """
    table = table.lower()

    if table in db.metadata.tables:
        gen = (v for k, v in db.Model._decl_class_registry.items() if k.lower() == table)
        cls: db.Model = next(gen, None)

        if cls:
            for item in cls.query.limit(5):
                print(item)
    else:
        print(f'{table} does not exist')
