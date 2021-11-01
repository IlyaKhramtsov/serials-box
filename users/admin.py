from django.contrib import admin

from users.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'name')
