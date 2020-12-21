from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    value = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.value


class Author(models.Model):
    value = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.value


class Artist(models.Model):
    value = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.value


class Comic(models.Model):
    class Types(models.IntegerChoices):
        OTHER = 0, _('Other')
        MANGA = 1, _('Manga')
        MANWHA = 2, _('Manwha')
        MANHUA = 3, _('Manhua')
        WESTERN = 4, _('Western')

    class ReadingOrder(models.IntegerChoices):
        RIGHT_TO_LEFT = 0, _('Right to Left')
        LEFT_TO_RIGHT = 1, _('Left to Right')
        VERTICAL = 2, _('Vertical')

    name = models.CharField(max_length=256)

    comic_type = models.IntegerField(
        choices=Types.choices, default=Types.OTHER)
    description = models.TextField(blank=True, null=True)
    reading_order = models.IntegerField(
        choices=ReadingOrder.choices, default=ReadingOrder.RIGHT_TO_LEFT)

    # Metadata
    tags = models.ManyToManyField(Tag, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    artists = models.ManyToManyField(Artist, blank=True)


class Chapter(models.Model):
    title = models.CharField(max_length=64)
    chapter_id = models.CharField(max_length=32)
    comic = models.ForeignKey(
        Comic, related_name='chapters', on_delete=models.CASCADE)
    page_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('chapter_id',)

    def __str__(self):
        return self.title


class Page(models.Model):
    file = models.FileField(verbose_name='File')
    chapter = models.ForeignKey(
        Chapter, related_name='pages', on_delete=models.CASCADE)
