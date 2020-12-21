from rest_framework import serializers

from myuri.models import Comic, Chapter


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('id', 'name', 'comic_type', 'description',
                  'reading_order', 'tags', 'authors', 'artists')


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['title', 'chapter_id', 'comic', 'page_count']
