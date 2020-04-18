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


def test_comic_exists_false(temp_folder):
    parser = ArchiveParser(temp_folder)

    exists = parser.comic_exists(1)
    assert not exists


def test_comic_exists_true(temp_folder):
    create_folder(temp_folder, 'comics', '42')

    parser = ArchiveParser(temp_folder)

    exists = parser.comic_exists(42)
    assert exists


def test_create_comic(temp_folder):
    parser = ArchiveParser(temp_folder)

    parser.create_comic(1)

    new_path = temp_folder / pathlib.Path('comics/1')
    assert new_path.exists()


def test_save_chapter(temp_folder):
    # populate with mock data
    create_folder(temp_folder, 'comics', '1')
    os.mkdir(temp_folder / 'mock')

    # create mock chapter
    mock_file = temp_folder / 'mock' / '0005.jpeg'
    mock_file.touch()
    with mock_file.open('wb') as file:
        file.write(b'foo')

    # create mock zip
    mock_zip = temp_folder / 'mock' / 'mock.cbr'
    with zipfile.ZipFile(mock_zip.resolve(), 'w') as file:
        file.write(mock_file, arcname='0005.jpeg')

    # call test func
    parser = ArchiveParser(temp_folder)
    with mock_zip.open('rb') as file:
        parser.save_chapter(1, 'foo', file)

    # assert cbr is created
    new_chapter_path = temp_folder / 'comics' / '1' / 'chap_foo.cbr'
    assert new_chapter_path.exists()

    # assert contains file
    with zipfile.ZipFile(new_chapter_path.resolve(), 'r') as file:
        assert file.read('0005.jpeg') == b'foo'