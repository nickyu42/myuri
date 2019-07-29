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
"""
import os
from typing import Optional
from pathlib import Path

DATA_FOLDER = Path(os.environ.get('DATA_FOLDER', default='./data'))


def get_page(comic_id: int, chapter: int, page: int) -> Optional[Path]:
    files = list(DATA_FOLDER.glob(f'comics/{comic_id}/chap_{chapter}/{page:0>4}.jpg'))

    if files:
        return files[0]

    return None


