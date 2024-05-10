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

    class StatusType(models.TextChoices):
        admin = 'admin', 'admin'
        manager = 'manager', 'manager'
        realize = 'Реализован', 'Реализован'
        unrealize = 'Не реализован', 'Не реализован'
        work_with_request = 'В работе, связался', 'В работе, связался'
        work_no_request = 'В работе, не связался', 'В работе, не связался'

    id = models.AutoField(primary_key=True, db_index=True)
    fio = models.CharField(max_length=64, null=True, blank=True)

    user_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    status = models.CharField(choices=StatusType, max_length=32, null=True)
    manager = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display = self.fio
        if not display:
            display = self.username
            if not display:
                return f'{self.id}'
        return display


class UserLog(models.Model):
    class Meta:
        db_table = 'users_logs'
        ordering = ['created_at']
        verbose_name = 'Логи  пользователей'
        verbose_name_plural = verbose_name


    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
    state = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    class Meta:
        db_table = 'requests'
        ordering = ['-created_at']
        verbose_name = 'Заявки для менеджеров'
        verbose_name_plural = verbose_name

    class RequestType(models.TextChoices):
        calculator = 'calculator', 'calculator'
        manager_help = 'manager_support', 'manager_support'

    id = models.CharField(max_length=8, primary_key=True)
    user = models.ForeignKey('User', to_field='user_id', related_name='requests_user', on_delete=models.CASCADE)
    type = models.CharField(choices=RequestType, max_length=64, null=True)

    calculator_data = models.CharField(max_length=4096, blank=True, null=True)
    calculator_photo = models.CharField(max_length=256, blank=True, null=True)

    support_data = models.CharField(max_length=4096, blank=True, null=True)
    has_worked = models.CharField(max_length=8, blank=True, null=True)
    from_where = models.CharField(max_length=64, blank=True, null=True)

    manager_answer = models.CharField(max_length=4096, blank=True, null=True)
    manager = models.ForeignKey('User', to_field='user_id', related_name='requests_manager', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FAQ(models.Model):
    class Meta:
        db_table = 'faq'
        ordering = ['id']
        verbose_name = 'Вопросы и ответы'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True)
    question = models.TextField(max_length=512)
    video_file_id = models.CharField(max_length=256)
    order_priority = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.id}'


class Dispatcher(models.Model):
    class Meta:
        db_table = 'mailings'
        ordering = ['id']
        verbose_name = 'Рассылки'
        verbose_name_plural = verbose_name

    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey('Post', to_field='id', on_delete=models.CASCADE)
    is_notification = models.BooleanField(default=False)
    is_for_all_users = models.BooleanField(default=False)
    status = models.CharField(choices=User.StatusType, max_length=32, null=True, blank=True)
    send_at = models.DateTimeField()

    def __str__(self):
        return f'{self.id}'


class Post(models.Model):
    class Meta:
        db_table = 'static_content'
        ordering = ['id']
        verbose_name = 'Контент для рассылок'
        verbose_name_plural = verbose_name

    id = models.BigIntegerField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=256, blank=True, null=True)  # to understand what does post mean
    photo_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_note_id = models.CharField(max_length=256, blank=True, null=True)
    document_file_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


class NotificationsSettings(models.Model):
    class Meta:
        db_table = 'notification_settings'
        ordering = ['id']
        verbose_name = 'Настройка уведомлений'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name='Текст')
    is_turn = models.BooleanField(default=False, verbose_name='Рассылка включена?')
