"""
Author: Nick Yu
Date Created: 7/29/2019

Folder structure parser

current structure is defined as:
root <- DATA_FOLDER/comics/<COMIC>
<COMIC> <- <VOLUME> | <CHAPTER>
<VOLUME> <- <CHAPTER> | <PAGE>
<CHAPTER> <- <PAGE>

name formats:
<COMIC> = <Comic.id>/
<VOLUME> = vol_<Volume.number>/
<CHAPTER> = chap_<Chapter.number>/
<PAGE> = {Page.number:0>4}.(jpg|jpeg|png)

range restrictions:
<Page.number> = >1
<Comic.id> = >1
"""
from typing import Union, BinaryIO, Tuple, IO
from pathlib import Path
from abc import ABC, abstractmethod

# File can either be a path to a file or an open IO object with file type
FileLike = Union[Path, Tuple[BinaryIO, str]]


class ComicException(Exception):
    pass


class AbstractComicParser(ABC):
    data_path: Path

    def __init__(self, data_path: Path):
        super(AbstractComicParser, self).__init__()
        self.data_path = data_path

    @abstractmethod
    def get_volume_page(self, comic_id: int, volume: str, page: int) -> FileLike:
        ...

    @abstractmethod
    def get_page(self, comic_id: int, chapter: str, page: int) -> FileLike:
        ...

    @abstractmethod
    def get_cover(self, comic_id: int) -> FileLike:
        ...

    @abstractmethod
    def comic_exists(self, comic_id: int) -> bool:
        ...

    @abstractmethod
    def create_comic(self, comic_id: int):
        ...

    @abstractmethod
    def save_chapter(self, comic_id: int, chapter: str, comic_file: IO):
        ...

    @abstractmethod
    def save_page(self, comic_id: int, page_file: IO):
        ...
