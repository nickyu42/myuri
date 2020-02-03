import os
import re
import zipfile
import click
from pathlib import Path

from flask.cli import AppGroup

data_cli = AppGroup('data')


def import_archive_volume(path: Path, name: str, overwrite=False):
    """
    Creates a new archive file in the data folder with the pages added
    The pages are sorted alphabetically based on filename
    """
    data_folder = os.environ.get('DATA_FOLDER', default='./data')

    if not os.path.exists(data_folder):
        try:
            os.mkdir(data_folder)
        except Exception as e:
            raise ValueError(f'Error occurred while attempting to create {data_folder}: {e}')

    new_archive_path = os.path.join(data_folder, name)
    if os.path.exists(new_archive_path) and not overwrite:
        raise ValueError(f'File: {new_archive_path} already exists and no overwrite specified')

    pattern = re.compile(r'.*\.((jpg)|(png)|(jpeg))')
    path_str = str(path.resolve())

    with zipfile.ZipFile(new_archive_path, mode='w') as new_file:
        files = os.listdir(path_str)
        files.sort()

        for i, page in enumerate(files):
            print(page)
            if pattern.match(page):
                page_filename = f'{i:0>4}{os.path.splitext(page)[-1]}'
                new_file.write(os.path.join(path_str, page), arcname=page_filename)


@data_cli.command('import_vol')
@click.argument('path')
@click.argument('name')
def import_vol(path: str, name: str):
    import_archive_volume(Path(path), name)
