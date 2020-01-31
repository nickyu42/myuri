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

import pytest

from data.archive_parser import ArchiveParser


@pytest.fixture
def temp_folder():
    temp_dir = tempfile.mkdtemp()
    yield pathlib.Path(temp_dir)
    shutil.rmtree(temp_dir)


def test_get_page(temp_folder):
    # populate with mock data
    temp_chap = pathlib.Path(f'{temp_folder.resolve()}/comics/1/chap_test.cbr')
    temp_chap.touch()

    # add fake page
    temp_page = pathlib.Path(f'{temp_folder.resolve()}/mock/0001.jpg')
    zipfile.ZipFile(temp_chap).write(temp_page)

    parser = ArchiveParser(temp_folder)
    page = parser.get_page(1, 'test', 1)
