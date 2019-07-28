"""
Author: Nick Yu
Date created: 23/7/2019
"""
import click
import os
from flask.cli import AppGroup

from app.database.models import *

db_cli = AppGroup('db')


@db_cli.command('reset')
def reset():
    """Setup data persistence"""
    database_name = os.environ.get('DB_NAME')

    if not database_name:
        print('DB_NAME is not defined in environment, defaulting to \'db\'')
        database_name = 'db'

    path = os.path.realpath(f'data/{database_name}.db')

    if os.path.exists(path):
        while True:
            inp = input(f'{path} already exists, reset tables? (y/n) ').lower()

            if inp in ('y', 'n'):
                break

        if inp == 'y':
            db.drop_all()
            db.create_all()
            print('Reset tables')
    else:
        try:
            # ignore FileExistsError
            os.mkdir('data')
        except FileExistsError:
            pass

        db.create_all()
        print('Created tables')


@db_cli.command('remove')
def remove():
    """Removes database entirely"""
    database_name = os.environ.get('DB_NAME')

    if not database_name:
        print('DB_NAME is not defined in environment, cancelling')
        return

    path = os.path.realpath(f'data/{database_name}.db')

    inp = input(f'Are you sure you want to remove {path}? (type y to confirm) ')

    if inp == 'y':
        os.remove(path)
        print('Removed')


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
