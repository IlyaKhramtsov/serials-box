from django.contrib import admin

from serials.models import Category, Comment, Crew, Genre, TVSeries


@admin.register(TVSeries)
class TVSerialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'poster', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('series', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('text',)
