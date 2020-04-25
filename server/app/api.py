"""
Author: Nick Yu
Date created: 19/7/2019
"""
from pathlib import Path
from typing import Optional

import werkzeug
from flask import request, Blueprint, send_file, json, Response, current_app, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS
from sqlalchemy.exc import DatabaseError

import app.database.models as models
from app.data.base_parser import AbstractComicParser, ComicException
from app.database import db


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
    """Endpoint for getting a JSON object with info on given chapter"""

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


class CreateComic(Resource):
    """POST Endpoint for creating new comics"""
    parser: AbstractComicParser
    req_parser: reqparse.RequestParser

    def __init__(self, **kwargs):
        self.parser = kwargs.get('parser')
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('comic_name', type=str, required=True, help='Name cannot be empty')

    def post(self):
        name = self.req_parser.parse_args()['comic_name']
        comic = models.Comic()
        db.session.add(comic)
        try:
            db.session.flush()
            comic_name = models.ComicName(name=name, comic_id=comic.id)
            db.session.add(comic_name)

            db.session.commit()
        except DatabaseError:
            db.session.rollback()
            abort(500, message=f'Creating comic with name={name} failed')

        self.parser.create_comic(comic.id)

        return jsonify({'id': comic.id})


class UploadComic(Resource):
    """POST Endpoint for uploading new comics"""
    parser: AbstractComicParser
    req_parser: reqparse.RequestParser

    def __init__(self, **kwargs):
        self.parser = kwargs.get('parser')
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('comic_name', type=str, required=True, help='Name cannot be empty')
        self.req_parser.add_argument('file_type', type=str, required=True, help='File type cannot be empty')
        self.req_parser.add_argument('upload_type', type=str, required=True,
                                     help='Missing type of "chapter" or "page"')
        self.req_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, required=True,
                                     help='Comic File cannot be empty', location='files')

        # only necessary in case of 'chapter' upload type
        self.req_parser.add_argument('chapter', type=str)

        # TODO automatically infer the amount of pages
        # since the file is in zip/rar format, it should be retrievable from the headers
        # another solution would be to unpack the compressed file on client side and
        # make this request force the user to upload pages separately
        self.req_parser.add_argument('total_pages', type=int)

    def post(self):
        args = self.req_parser.parse_args()

        file: werkzeug.datastructures.FileStorage = args['file']
        comic_name = args['comic_name']

        # check if comic with name exists
        comic_name = models.ComicName.query.filter(models.ComicName.name == comic_name).scalar()

        if not comic_name:
            abort(400, message=f'Comic with name={comic_name} does not exist')

        comic_id = comic_name.id

        # store comic in data folder
        if args['upload_type'] == 'chapter':
            if args['chapter'] is None:
                abort(400, message=f'upload_type=chapter, but "chapter" argument missing')

            if args['total_pages'] is None:
                abort(400, message=f'upload_type=chapter, but "total_pages" argument missing')

            self.save_chapter(comic_id, args['chapter'], args['total_pages'], file)
            return 200

        elif args['upload_type'] == 'page':
            return abort(501, message=f'upload_type=page is currently not supported')

    def save_chapter(self, comic_id: int, chapter_nr: str, pages: int, file: werkzeug.datastructures.FileStorage):
        # create chapter meta
        chapter = models.Chapter(number=chapter_nr, comic_id=comic_id, total_pages=pages)
        db.session.add(chapter)
        try:
            # attempt to store the chapter and commit to db
            self.parser.save_chapter(comic_id, chapter_nr, file.stream)
            db.session.commit()
        except ComicException as e:
            db.session.rollback()
            abort(500, message=f'Uploading failed with error: {str(e)}')
        except DatabaseError:
            db.session.rollback()
            abort(500, message=f'Uploading failed')


def create_api(data_parser: AbstractComicParser) -> Blueprint:
    api_routes = Blueprint('api', __name__)
    CORS(api_routes)

    api = Api(api_routes)

    api.add_resource(Catalog, '/catalog')
    api.add_resource(Info, '/info/<int:comic_id>')
    api.add_resource(ChapterInfo, '/info/chap/<string:chapter_nr>')
    api.add_resource(Cover, '/cover/<int:comic_id>', resource_class_kwargs={'parser': data_parser})
    api.add_resource(Page, '/<int:comic_id>/<string:chapter_nr>/<int:page>',
                     resource_class_kwargs={'parser': data_parser})

    api.add_resource(CreateComic, '/create_comic', resource_class_kwargs={'parser': data_parser})
    api.add_resource(UploadComic, '/upload', resource_class_kwargs={'parser': data_parser})

    return api_routes
