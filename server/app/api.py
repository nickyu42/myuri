"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import request, Blueprint, send_file
from flask_restful import Api, Resource
from typing import Optional

import app.database.models as models
from app.data import get_page


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

        # TODO change error to 404 error instead of JSON object
        if not comic:
            return {'error': f'Comic with id={comic_id} does not exist'}

        return comic.json


class Page(Resource):
    """Endpoint for getting images from comics"""

    @staticmethod
    def get(comic_id: int, chapter: int, page: int):
        comic: Optional[models.Comic] = models.Comic.query.get(comic_id)

        if not comic:
            return {'error': f'Comic with id={comic_id} does not exist'}

        path = get_page(comic.id, chapter, page)

        if not path:
            return {'error': f'Page {page} of chapter {chapter} could not be found for {comic_id}'}

        return send_file(path.resolve(), 'image/jpg')


api_routes = Blueprint('api', __name__)
api = Api(api_routes)

api.add_resource(Catalog, '/c/catalog')
api.add_resource(Info, '/c/info/<int:comic_id>')
api.add_resource(Page, '/c/<int:comic_id>/<int:chapter>/<int:page>')
