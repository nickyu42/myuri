from django.views import generic

from myuri.models import Comic


class ComicDetail(generic.DetailView):
    model = Comic
