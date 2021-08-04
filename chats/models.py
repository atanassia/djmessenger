#from django.contrib.auth.models import User

from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


# def generate_unique_code():
#     return ''.join(str(uuid.uuid4()).split('-'))


class Chat(models.Model):

    # code = models.CharField(
    #     max_length=32,
    #     unique=True,
    #     blank = True,
    #     default=generate_unique_code,
    #     verbose_name = 'Код для входа'
    # )
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200, blank = True, default = "Чат", verbose_name = 'Название')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'chatusers', verbose_name = 'Участники')
    #image = models.ImageField(upload_to = 'images/chats/%Y/%m', blank = False, null=True, verbose_name = 'Изображение чата')
    is_dialog = models.BooleanField(null=False, default=False, verbose_name= 'Диалог')
    members_count = models.IntegerField(default = 0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name = 'Количество участников')
    created = models.DateTimeField(auto_now_add=True, verbose_name= 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name= 'Обновлен')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-created', 'updated']

    def __str__(self):
        return self.name
   
    def clean(self): 
        if self.is_dialog == True:
            self.members_count = 2

    def get_absolute_url(self):
        return reverse("chat", kwargs={"code": self.code})


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, 
        on_delete = models.PROTECT, 
        related_name = 'message',
        verbose_name = 'Чат'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.PROTECT, 
        related_name = 'message', 
        verbose_name = 'Отправитель'
    )
    message = models.CharField(max_length=3000, verbose_name = 'Сообщение')
    is_readed = models.BooleanField(default=False, verbose_name = 'Прочитано')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Обновлен')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created', 'updated']
    
    def __str__(self):
        return self.message