from app.data.base_parser import AbstractComicParser, FileLike, ComicException


class ComicParser(AbstractComicParser):
    def get_volume_page(self, comic_id: int, volume: str, page: int) -> FileLike:
        files = list(self.data_path.glob(f'comics/{comic_id}/vol_{volume}/{page:0>4}.*'))

        if files:
            return files[0]
        else:
            # TODO make it so that volumes can contain chapters, so parsing a page should visit a chapter
            pass

        raise ComicException(f'comics/{comic_id}/vol_{volume}/{page:0>4}.* does not exist')

    def get_page(self, comic_id: int, chapter: str, page: int) -> FileLike:
        files = list(self.data_path.glob(f'comics/{comic_id}/chap_{chapter}/{page:0>4}.*'))

        if files:
            return files[0]

        raise ComicException(f'comics/{comic_id}/chap_{chapter}/{page:0>4}.* does not exist')

    def get_cover(self, comic_id: int) -> FileLike:
        files = list(self.data_path.glob(f'comics/{comic_id}/thumbnail.*'))

        if files:
            return files[0]

        raise ComicException(f'comics/{comic_id}/thumbnail.* does not exist')
