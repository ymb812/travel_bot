import string
import random
from django.db import models
from admin_panel_for_bot.settings import settings


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class User(models.Model):
    class Meta:
        db_table = 'users'
        ordering = ['created_at']
        verbose_name = 'Пользователи'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True, db_index=True)
    fio = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=64, unique=True, null=True, blank=True)

    user_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display = self.username
        if not display:
            return f'{self.id}'
        return display


class Dispatcher(models.Model):
    class Meta:
        db_table = 'mailings'
        ordering = ['id']
        verbose_name = 'Рассылки'
        verbose_name_plural = verbose_name

    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey('Post', to_field='id', on_delete=models.CASCADE)
    is_notification = models.BooleanField(default=False)
    send_at = models.DateTimeField()

    def __str__(self):
        return f'{self.id}'


class Request(models.Model):
    class Meta:
        db_table = 'requests'
        ordering = ['id']
        verbose_name = 'Заявки для менеджеров'
        verbose_name_plural = verbose_name

    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
    type = models.CharField(max_length=64, null=True)
    has_worked = models.CharField(max_length=8, null=True)
    from_where = models.CharField(max_length=64, null=True)

    calculator_data = models.CharField(max_length=4096, null=True)
    calculator_photo = models.CharField(max_length=256, null=True)

    is_in_process = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    class Meta:
        db_table = 'static_content'
        ordering = ['id']
        verbose_name = 'Контент для рассылок'
        verbose_name_plural = verbose_name

    id = models.BigIntegerField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=256, blank=True, null=True) # to understand what does post mean
    photo_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_note_id = models.CharField(max_length=256, blank=True, null=True)
    document_file_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
