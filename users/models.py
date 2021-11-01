from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    email = models.EmailField(max_length=200, verbose_name='Email')
    message = models.TextField(max_length=1000, verbose_name='Сообщение')

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.email
