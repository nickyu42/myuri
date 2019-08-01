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
from typing import Optional
from pathlib import Path
from abc import ABC, abstractmethod


class AbstractComicParser(ABC):
    def __init__(self, data_path: Path):
        self.data_path = data_path
        super(AbstractComicParser, self).__init__()

    @abstractmethod
    def get_volume_page(self, comic_id: int, volume: str, page: int) -> Optional[Path]:
        ...

    @abstractmethod
    def get_page(self, comic_id: int, chapter: str, page: int) -> Optional[Path]:
        ...

    @abstractmethod
    def get_thumbnail(self, comic_id: int) -> Optional[Path]:
        ...


class ComicParser(AbstractComicParser):
    def get_volume_page(self, comic_id: int, volume: str, page: int) -> Optional[Path]:
        files = list(self.data_path.glob(f'comics/{comic_id}/vol_{volume}/{page:0>4}.*'))

        if files:
            return files[0]
        else:
            # TODO make it so that volumes can contain chapters, so parsing a page should visit a chapter
            pass

        return None

    def get_page(self, comic_id: int, chapter: str, page: int) -> Optional[Path]:
        files = list(self.data_path.glob(f'comics/{comic_id}/chap_{chapter}/{page:0>4}.*'))

        if files:
            return files[0]

        return None

    def get_thumbnail(self, comic_id: int) -> Optional[Path]:
        files = list(self.data_path.glob(f'comics/{comic_id}/thumbnail.*'))

        if files:
            return files[0]

        return None


