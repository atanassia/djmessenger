from django.db import models
from django.conf import settings
#from django.utils import timezone



class DialogMessages(models.Model):
    dialog = models.ForeignKey(
        'Dialog', 
        on_delete = models.PROTECT, 
        related_name = 'dialog',
        verbose_name = 'Диалог'
    )
    dialog_sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.PROTECT, 
        related_name = 'dialog_sender', 
        verbose_name = 'Отправитель'
    )
    message = models.CharField(max_length=3000, verbose_name = 'Сообщение')
    is_readed = models.BooleanField(default=False, verbose_name = 'Прочитано')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Обновлен')

    class Meta:
        verbose_name = 'Сообщение диалога'
        verbose_name_plural = 'Сообщения диалога'
        ordering = ['-created', 'updated']
    
    def __str__(self):
        return self.message


class Dialog(models.Model):
    first_opponent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.PROTECT, 
        related_name = 'first_opponent', 
        verbose_name = 'Первый пользователь'
    )
    second_opponent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.PROTECT, 
        related_name = 'second_opponent', 
        verbose_name = 'Второй пользователь'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name= 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name= 'Обновлен')
    #FIXME: можно почему-то создать диалог двойной, то бишь с user1 и user2 А ТАКЖЕ user2 и user1
    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'
        ordering = ['-created', 'updated']
        unique_together = [
            ['first_opponent', 'second_opponent'],
            ['second_opponent', 'first_opponent']
        ]

    def __str__(self):
        return f"{self.first_opponent} + {self.second_opponent}"



class ChatMessages(models.Model):
    chat = models.ForeignKey(
        'Chat', 
        on_delete = models.PROTECT, 
        related_name = 'Chat',
        verbose_name = 'Чат'
    )
    chat_sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.PROTECT, 
        related_name = 'chat_sender', 
        verbose_name = 'Отправитель'
    )
    message = models.CharField(max_length=3000, verbose_name = 'Сообщение')
    is_readed = models.BooleanField(default=False, verbose_name = 'Прочитано')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Обновлен')

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        ordering = ['-created', 'updated']
    
    def __str__(self):
        return self.message


class Chat(models.Model):
    name = models.CharField(max_length = 200, blank = False, verbose_name = 'Название')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'creator', on_delete = models.PROTECT, verbose_name = 'Создатель чата')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'users', verbose_name = 'Участники')
    image = models.ImageField(upload_to = 'images/chats/%Y/%m', verbose_name = 'Изображение чата')
    slug = models.SlugField(max_length=100, unique = True, verbose_name = 'Слаг чата')
    created = models.DateTimeField(auto_now_add=True, verbose_name= 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name= 'Обновлен')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-created', 'updated']

    def __str__(self):
        return self.name

    