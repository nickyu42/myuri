from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from myuri.models import Comic
from myuri.serializers import ComicSerializer


class APIComicList(generics.ListCreateAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['tags', 'artists', 'authors']
    search_fields = ['name', 'description']


class APIComicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
