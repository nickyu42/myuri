import zipfile
import re
import os
from pathlib import Path

from data.base_parser import FileLike, ComicException
from data.file_parser import ComicParser


class ArchiveParser(ComicParser):

    def get_page(self, comic_id: int, chapter: str, page: int) -> FileLike:
        files = list(self.data_path.glob(f'comics/{comic_id}/chap_{chapter}.cbr'))

        if files:
            filepath = files[0]
            return self.get_zip_page(filepath, page)

        raise ComicException(f'comics/{comic_id}/chap_{chapter}.cbr does not exist')

    def get_volume_page(self, comic_id: int, volume: str, page: int) -> FileLike:
        # TODO add caching of files to prevent constant zip unpacking
        files = list(self.data_path.glob(f'comics/{comic_id}/vol_{volume}.cbr'))

        if files:
            filepath = files[0]
            return self.get_zip_page(filepath, page)

        raise ComicException(f'comics/{comic_id}/vol_{volume}.cbr does not exist')

    @staticmethod
    def get_zip_page(filepath: Path, page: int) -> FileLike:
        try:
            root_archive = zipfile.ZipFile(filepath.resolve())
            pages = root_archive.namelist()
            pattern = re.compile(f'{page:0>4}.(jpg)|(png)|(jpeg)')

            matched = list(filter(pattern.match, pages))

            if matched:
                file_extension = os.path.splitext(matched[0])[-1]
                with root_archive.open(matched[0]) as f:
                    return f, file_extension

        except zipfile.BadZipFile as e:
            raise ComicException(f'{filepath} could not be opened\n{str(e)}')