from typing import Callable

from django.contrib import admin
from django.db import models

from myuri.models import *


def add_display(*fields: str) -> Callable:
    """
    Decorater that adds functionality for viewing relational fields.
    Adds functions to given class that return the string representation of ``fields``.
    """
    def wrapped(klass):
        for field in fields:
            setattr(klass, f'{field}_str', lambda self, obj: ', '.join(
                str(x) for x in getattr(obj, field).all()))

        return klass

    return wrapped


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'comic')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('value',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('value',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('value',)
