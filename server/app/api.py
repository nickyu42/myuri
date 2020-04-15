"""
Author: Nick Yu
Date created: 19/7/2019
"""
from pathlib import Path
from typing import Optional
from flask import request, Blueprint, send_file, jsonify, json, Response, current_app
from flask_restful import Api, Resource, abort
from flask_cors import CORS

import app.database.models as models
from app.data.base_parser import AbstractComicParser, ComicException


def jsonify_str(obj):
    """Drop-in for jsonify where default serializer is str()"""

    json_data = json.dumps(obj, indent=None, separators=(',', ':'), default=str)
    return Response(json_data, mimetype=current_app.config['JSONIFY_MIMETYPE'])


class Catalog(Resource):
    """Endpoint for getting a JSON catalog based on the query given"""

    @staticmethod
    def get():
        args = request.args
        return str(args)


class Info(Resource):
    """Endpoint for getting a JSON object with info on given comic"""

    @staticmethod
    def get(comic_id: int):
        comic: Optional[models.Comic] = models.Comic.query.get(comic_id)

        if not comic:
            abort(404, message=f'Comic with id={comic_id} does not exist')

        comic_obj = comic.to_obj()
        comic_obj['names'] = [n.name for n in comic_obj['names']]

        return jsonify_str(comic_obj)


class ChapterInfo(Resource):

    @staticmethod
    def get(chapter_nr: str):
        chapter: Optional[models.Chapter] = models.Chapter.query.filter(models.Chapter.number == '1').scalar()

        if not chapter:
            abort(404, message=f'Chapter with nr={chapter_nr} does not exist')

        return jsonify_str(chapter.to_obj())


class Page(Resource):
    """Endpoint for getting images from comics"""
    parser: AbstractComicParser

    def __init__(self, **kwargs):
        self.parser = kwargs.get('parser')

        if not self.parser:
            raise ValueError('Parser not provided')

    def get(self, comic_id: int, chapter_nr: str, page: int):
        comic: Optional[models.Comic] = models.Comic.query.get(comic_id)

        if not comic:
            abort(404, message=f'Comic with id={comic_id} does not exist')

        try:
            page = self.parser.get_page(comic.id, chapter_nr, page)

            if isinstance(page, Path):
                image_type = page.suffix[1:]
                return send_file(page.resolve(), f'image/{image_type}')

            file, file_extension = page
            file_extension = file_extension.replace('.', '')

            # in the case where file is a BytesIO send_file in wsgi will fail
            # this is due to a wsgi optimization on file_descriptors, however BytesIO is not a fd
            # wsgi-file-wrapper needs to be disabled
            return send_file(file, f'image/{file_extension}')

        except ComicException:
            abort(404, message=f'Page {page} of chapter {chapter_nr} could not be found for {comic_id}')


class Cover(Resource):
    """Endpoint for getting a comic cover"""
    parser: AbstractComicParser

    def __init__(self, **kwargs):
        self.parser = kwargs.get('parser')

        if not self.parser:
            raise ValueError('Parser not provided')

    def get(self, comic_id: int):
        comic: Optional[models.Comic] = models.Comic.query.get(comic_id)

        if not comic:
            abort(404, message=f'Comic with id={comic_id} does not exist')

        path = self.parser.get_cover(comic_id)

        if not path:
            abort(404, message=f'Thumbnail for {comic_id} does not exist')

        image_type = path.suffix[1:]
        return send_file(path.resolve(), f'image/{image_type}')


def create_api(data_parser: AbstractComicParser) -> Blueprint:
    api_routes = Blueprint('api', __name__)
    CORS(api_routes)

    api = Api(api_routes)

    api.add_resource(Catalog, '/catalog')
    api.add_resource(Info, '/info/<int:comic_id>')
    api.add_resource(ChapterInfo, '/info/chap/<string:chapter_nr>')
    api.add_resource(Page, '/<int:comic_id>/<string:chapter_nr>/<int:page>',
                     resource_class_kwargs={'parser': data_parser})
    api.add_resource(Cover, '/cover/<int:comic_id>',
                     resource_class_kwargs={'parser': data_parser})

    return api_routes
