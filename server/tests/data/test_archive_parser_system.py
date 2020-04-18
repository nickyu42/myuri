"""
Author: Nick Yu
Date Created: 18/4/2020

Test suite for cbr reading system tests
"""
import os
import shutil
import pathlib
import tempfile
import zipfile
from typing import Iterable, BinaryIO

import pytest

from app.data.archive_parser import ArchiveParser


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


def test_save_chapter(temp_folder):
    # populate with mock data
    parser = ArchiveParser(temp_folder)

    parser.create_comic(1)

    # create mock zip
    mock_zip = temp_folder / 'mock.cbr'
    mock_zip.touch()
    with zipfile.ZipFile(mock_zip.resolve(), 'w') as file:
        file.writestr('0002.jpeg', b'foo')

    # call test func
    with mock_zip.open('rb') as file:
        parser.save_chapter(1, 'foo', file)

    f, extension = parser.get_page(1, 'foo', 2)

    assert f.read() == b'foo'
