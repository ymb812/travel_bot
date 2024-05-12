import logging
from enum import Enum
from datetime import datetime
from tortoise import fields
from tortoise.models import Model
from enum import Enum


logger = logging.getLogger(__name__)


class User(Model):
    class Meta:
        table = 'users'
        ordering = ['created_at']

    class StatusType(Enum):
        admin = 'admin'
        manager = 'manager'
        realize = 'Реализован'
        unrealize = 'Не реализован'
        work_with_request = 'В работе, связался'
        work_no_request = 'В работе, не связался'

    id = fields.IntField(pk=True, index=True)
    fio = fields.CharField(max_length=64, null=True)

    user_id = fields.BigIntField(null=True, unique=True)
    username = fields.CharField(max_length=32, null=True)
    status = fields.CharField(
        choices=[(tag.value, tag.name) for tag in StatusType],
        max_length=32,
        default=StatusType.work_no_request.value,
    )
    manager = fields.ForeignKeyField('models.User', to_field='user_id', null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @classmethod
    async def update_data(cls, user_id: int, username: str):
        user = await cls.filter(user_id=user_id).first()
        if user is None:
            user = await cls.create(
                user_id=user_id,
                username=username,
            )
        else:
            await cls.filter(user_id=user_id).update(
                username=username,
                updated_at=datetime.now(),
            )

        return user

    @classmethod
    async def update_admin_data(cls, user_id: int, username: str, status: str):
        user = await cls.get_or_none(user_id=user_id)
        if user is None:
            await cls.create(
                user_id=user_id,
                username=username,
                status=status
            )
        else:
            user.status = status
            await user.save()


class UserLog(Model):
    class Meta:
        table = 'users_logs'
        ordering = ['id']

    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField('models.User', to_field='user_id')
    state = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def create_log(
            cls,
            user_id: int,
            state: str,
    ):
        log = await cls.create(user_id=user_id, state=state)
        return log


class Request(Model):
    class Meta:
        table = 'requests'
        ordering = ['created_at']

    class RequestType(Enum):
        calculator = 'calculator'
        manager_support = 'manager_support'

    id = fields.CharField(max_length=8, pk=True)
    user = fields.ForeignKeyField('models.User', to_field='user_id', related_name='requests_user')
    type = fields.CharField(choices=[(tag.value, tag.name) for tag in RequestType], max_length=64, null=True)

    calculator_data = fields.CharField(max_length=4096, null=True)
    calculator_photo = fields.CharField(max_length=256, null=True)

    support_data = fields.CharField(max_length=4096, null=True)
    has_worked = fields.CharField(max_length=8, null=True)
    from_where = fields.CharField(max_length=64, null=True)

    manager_answer = fields.CharField(max_length=4096, null=True)
    manager = fields.ForeignKeyField('models.User', to_field='user_id', null=True, related_name='requests_manager')

    created_at = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def create_request(
            cls,
            id: str,
            user_id: int,
            type: "Request.RequestType",
            calculator_data: str | None = None,
            calculator_photo: str | None = None,
            support_data: str | None = None,
    ):
        request = await Request.create(
            id=id,
            user_id=user_id,
            type=type.value,
            calculator_data=calculator_data,
            calculator_photo=calculator_photo,
            support_data=support_data,
        )
        return request


class RequestLog(Model):
    class Meta:
        table = 'request_logs'
        ordering = ['-id']

    id = fields.BigIntField(pk=True)
    manager = fields.ForeignKeyField('models.User', to_field='user_id', related_name='managers_log')
    user = fields.ForeignKeyField('models.User', to_field='user_id', related_name='users_log')
    request = fields.ForeignKeyField('models.Request', to_field='id', null=True)  # null cuz we pin manager w/o request
    created_at = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def create_log(cls, manager_id: int, user_id: int, request_id: int = None):
        await cls.create(manager_id=manager_id, user_id=user_id, request_id=request_id)


class FAQ(Model):
    class Meta:
        table = 'faq'

    id = fields.BigIntField(pk=True)
    question = fields.CharField(max_length=512)
    video_file_id = fields.CharField(max_length=256)
    order_priority = fields.IntField(unique=True)


class Dispatcher(Model):
    class Meta:
        table = 'mailings'
        ordering = ['id']

    id = fields.BigIntField(pk=True)
    post = fields.ForeignKeyField('models.Post', to_field='id')
    is_notification = fields.BooleanField(default=False)
    is_for_all_users = fields.BooleanField(default=False)
    status = fields.CharField(max_length=32, null=True)  # mailings by user's status
    send_at = fields.DatetimeField()


class Post(Model):
    class Meta:
        table = 'static_content'

    id = fields.BigIntField(pk=True)
    text = fields.TextField(null=True)
    designation = fields.CharField(max_length=256, null=True)  # to understand what does post mean
    photo_file_id = fields.CharField(max_length=256, null=True)
    video_file_id = fields.CharField(max_length=256, null=True)
    video_note_id = fields.CharField(max_length=256, null=True)
    document_file_id = fields.CharField(max_length=256, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class NotificationsSettings(Model):
    class Meta:
        table = 'notification_settings'

    id = fields.BigIntField(pk=True)
    text = fields.TextField()
    is_turn = fields.BooleanField(default=True)
