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
from typing import Union, BinaryIO, Dict, Any, Tuple
from pathlib import Path
from abc import ABC, abstractmethod

FileLike = Union[Path, Tuple[BinaryIO, str]]


class ComicException(Exception):
    pass


class Cache:
    """
    Mark and sweep like cache object
    """
    cache: Dict[str, Any]
    counter: Dict[str, int]

    def __init__(self):
        self.cache = {}
        self.counter = {}

    def sweep(self):
        to_remove = filter(lambda _, v: v == 0, self.counter.items())

        for k, _ in to_remove:
            del self.cache[k]
            del self.counter[k]

    def add_item(self, key, value):
        self.cache[key] = value
        self.counter[key] = 1

    def decrease_reference(self, item):
        if item in self.counter and self.counter[item] > 0:
            self.counter[item] -= 1

    def increase_reference(self, item):
        if item in self.counter:
            self.counter[item] += 1

    def __getitem__(self, item):
        return self.cache[item]


class AbstractComicParser(ABC):
    data_path: Path
    file_cache: Cache

    def __init__(self, data_path: Path):
        super(AbstractComicParser, self).__init__()
        self.data_path = data_path
        self.file_cache = Cache()

    @abstractmethod
    def get_volume_page(self, comic_id: int, volume: str, page: int) -> FileLike:
        ...

    @abstractmethod
    def get_page(self, comic_id: int, chapter: str, page: int) -> FileLike:
        ...

    @abstractmethod
    def get_cover(self, comic_id: int) -> FileLike:
        ...
