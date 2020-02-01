"""
Author: Nick Yu
Date Created: 31/1/2020

Test suite for cbr reading
"""
import os
import shutil
import pathlib
import tempfile
import zipfile
from typing import Iterable

import pytest

from app.data.archive_parser import ArchiveParser
from app.data.base_parser import ComicException


@pytest.fixture
def temp_folder():
    """ Fixture that creates a temp directory """
    temp_dir = tempfile.mkdtemp()
    yield pathlib.Path(temp_dir)
    shutil.rmtree(temp_dir)


def create_folder(root: pathlib.Path, *path: Iterable[str]):
    """ Helper function for easy folder creation """
    full_path = root

    for p in path:
        full_path /= p
        os.mkdir(str(full_path.resolve()))

    return full_path


def test_get_page_success(temp_folder):
    # populate with mock data
    create_folder(temp_folder, 'comics', '1')

    # add mock page
    with zipfile.ZipFile(f'{temp_folder.resolve()}/comics/1/chap_test.cbr', 'w') as file:
        os.mkdir(temp_folder / 'mock')
        mock_file = temp_folder / 'mock' / '0001.jpeg'
        mock_file.touch()
        file.write(mock_file, arcname='0001.jpeg')

    parser = ArchiveParser(temp_folder)
    _, extension = parser.get_page(1, 'test', 1)

    assert extension == '.jpeg'


def test_get_volume_page(temp_folder):
    # populate with mock data
    create_folder(temp_folder, 'comics', '1')

    # add mock page
    with zipfile.ZipFile(f'{temp_folder.resolve()}/comics/1/vol_test.cbr', 'w') as file:
        os.mkdir(temp_folder / 'mock')
        mock_file = temp_folder / 'mock' / '0005.jpeg'
        mock_file.touch()
        file.write(mock_file, arcname='0005.jpeg')

    parser = ArchiveParser(temp_folder)
    _, extension = parser.get_volume_page(1, 'test', 5)

    assert extension == '.jpeg'


def test_get_page_missing(temp_folder):
    # populate with mock data
    create_folder(temp_folder, 'comics', '1')

    # add empty cbr
    with zipfile.ZipFile(f'{temp_folder.resolve()}/comics/1/chap_test.cbr', 'w'):
        pass

    parser = ArchiveParser(temp_folder)

    with pytest.raises(ComicException):
        parser.get_page(1, 'test', 1)

