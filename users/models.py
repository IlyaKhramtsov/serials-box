from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    email = models.EmailField(max_length=200, verbose_name='Email')
    message = models.TextField(max_length=1000, verbose_name='Сообщение')

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(upload_to="users", verbose_name="Фото")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return str(self.user)
