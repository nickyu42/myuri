"""
Author: Nick Yu
Date created: 23/7/2019
"""
import click
import os
from typing import List, Optional
from flask.cli import AppGroup

from app.database.models import *

db_cli = AppGroup('db')


def get_model(name: str) -> Optional[db.Model]:
    """
    Get Model if it exists
    :param name: name of the table to find
    :return: Type object of db.Model
    """
    name = name.lower()

    if name in db.metadata.tables:
        gen = (v for k, v in db.Model._decl_class_registry.items() if k.lower() == name)
        return next(gen, None)

    return None


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
    cls: db.Model = get_model(table)

    if cls:
        for item in cls.query.limit(5):
            print(item)
    else:
        print(f'{table} does not exist')


@db_cli.command('insert')
@click.argument('table')
@click.argument('args', nargs=-1)
def insert(table: str, args: List[str]):
    """
    Inserts given object into table
    Horribly hacky code!, should only ever be allowed for testing
    :param table: which table to insert to
    :param args: arguments, should be formatted as "<KEY>=<VAL>"
    """
    cls: BaseMixin = get_model(table)

    if cls:
        kwargs = {k: eval(v) for k, v in [tuple(a.split('=')) for a in args]}
        cls.create(**kwargs)
    else:
        print(f'{table} does not exist')