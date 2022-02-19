from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "time_create", "photo", "is_published")
    prepopulated_fields = {"slug": ("title",)}
