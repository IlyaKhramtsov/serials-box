import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Contact(models.Model):
    """Model representing the contact form."""
    name = models.CharField(max_length=200, verbose_name='Имя')
    email = models.EmailField(max_length=200, verbose_name='Email')
    message = models.TextField(max_length=1000, verbose_name='Сообщение')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Model representing the user's personal profile."""
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(
        upload_to='users', null=True, blank=True, verbose_name='Фото'
    )
    birthday = models.DateField(
        null=True, blank=True, verbose_name='День рождения'
    )
    city = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Город'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_age(self):
        """Calculates user's age."""
        today = datetime.date.today()
        return (today.year - self.birthday.year) - int(
            (today.month, today.day) <
            (self.birthday.month, self.birthday.day)
        )
