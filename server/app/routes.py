"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import Blueprint


main_page = Blueprint('main', __name__)


@main_page.route('/')
def index():
    return 'Hello World'
