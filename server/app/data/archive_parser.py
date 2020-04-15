import zipfile
import re
import os
import io
from pathlib import Path

from app.data.base_parser import FileLike, ComicException
from app.data.file_parser import ComicParser


class ArchiveParser(ComicParser):

    def get_page(self, comic_id: int, chapter: str, page: int) -> FileLike:

        filepath = self.data_path / Path(f'comics/{comic_id}/chap_{chapter}.cbr')

        if filepath.exists():
            return self.get_zip_page(filepath, page)

        raise ComicException(f'comics/{comic_id}/chap_{chapter}.cbr does not exist')

    def get_volume_page(self, comic_id: int, volume: str, page: int) -> FileLike:
        # TODO add caching of files to prevent constant zip unpacking
        filepath = self.data_path / Path(f'comics/{comic_id}/vol_{volume}.cbr')

        if filepath.exists():
            return self.get_zip_page(filepath, page)

        raise ComicException(f'comics/{comic_id}/vol_{volume}.cbr does not exist')

    def get_cover(self, comic_id: int) -> FileLike:
        files = list(self.data_path.glob(f'comics/{comic_id}/thumbnail.*'))

        if files:
            return files[0]

        raise ComicException(f'comics/{comic_id}/thumbnail.* does not exist')

    @staticmethod
    def get_zip_page(filepath: Path, page: int) -> FileLike:
        try:
            root_archive = zipfile.ZipFile(filepath.resolve())
            pages = root_archive.namelist()
            pattern = re.compile(f'{page:0>4}\\.((jpg)|(png)|(jpeg))')

            matched = list(filter(pattern.match, pages))

            if matched:
                file_extension = os.path.splitext(matched[0])[-1]
                with root_archive.open(matched[0]) as f:
                    # send a copy of the file, since it is closed after the return
                    return io.BytesIO(f.read()), file_extension

        except zipfile.BadZipFile as e:
            raise ComicException(f'{filepath.resolve()} could not be opened\n{str(e)}')

        raise ComicException(f'Page {page} could not be found in {filepath.resolve()}')
