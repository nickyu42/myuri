from django.views import generic

from myuri.models import Comic


class ComicList(generic.ListView):
    model = Comic
