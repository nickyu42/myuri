from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from myuri.models import Chapter
from myuri.serializers import ChapterSerializer


class APIChapterList(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['chapter_id', 'comic']
    search_fields = ['title']


class APIChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
