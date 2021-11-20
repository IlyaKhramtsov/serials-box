from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField


class TVSeries(models.Model):
    """Model representing TV series."""
    title = models.CharField(max_length=255, verbose_name="Название сериала")
    description = models.TextField(blank=True, verbose_name="Описание сериала")
    poster = models.ImageField(upload_to="serials", verbose_name="Постер")
    trailer = EmbedVideoField(verbose_name="Трейлер")
    year = models.PositiveSmallIntegerField(verbose_name="Дата выхода", default=2021)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    genres = models.ManyToManyField('Genre', verbose_name="Жанры")
    actors = models.ManyToManyField('Crew', verbose_name="Актеры", related_name="series_actors")
    directors = models.ManyToManyField('Crew', verbose_name="Режиссеры", related_name="series_directors")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    favorite = models.ManyToManyField(User, blank=True, verbose_name='Избранное', related_name='favorite')
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Get absolute URL for series."""
        return reverse('series_detail', kwargs={'series_slug': self.slug})


class Category(models.Model):
    """Model representing TV series categories."""
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get absolute URL for category."""
        return reverse('category', kwargs={'category_slug': self.slug})


class Genre(models.Model):
    """Model representing the genres of the series."""
    name = models.CharField(max_length=100, db_index=True, verbose_name="Жанр")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Crew(models.Model):
    """Model representing the cast and crew"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to="crew/", verbose_name="Фото")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('crew_detail', kwargs={"crew_slug": self.slug})


class Comment(models.Model):
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, verbose_name='Сериал', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    def __str__(self):
        return f'Комментарий от {self.author} на {self.series}'
