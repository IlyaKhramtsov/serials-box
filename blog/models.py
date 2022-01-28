from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField
from slugify import slugify


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = RichTextField(blank=True, null=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    likes = models.ManyToManyField(User, related_name='blog_articles', verbose_name='Лайки')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def total_likes(self):
        """Counts all likes for article."""
        return self.likes.count()

    def save(self, *args, **kwargs):
        """Makes auto slug and saves to database."""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute URL for articles."""
        return reverse('article_detail', kwargs={'article_slug': self.slug})

    def __str__(self):
        return self.title
