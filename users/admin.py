from django.contrib import admin

from users.models import Contact, Profile


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')

