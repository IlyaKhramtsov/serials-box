from django.contrib import admin

from serials.models import Category, Crew, Genre, TVSeries

admin.site.register(Category)
admin.site.register(Crew)
admin.site.register(Genre)
admin.site.register(TVSeries)
