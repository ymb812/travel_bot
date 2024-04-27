import logging
import uuid
from datetime import datetime
from tortoise import fields
from tortoise.models import Model
from enum import Enum


logger = logging.getLogger(__name__)


class User(Model):
    class Meta:
        table = 'users'
        ordering = ['created_at']

    id = fields.IntField(pk=True, index=True)
    fio = fields.CharField(max_length=64, null=True)

    user_id = fields.BigIntField(null=True, unique=True)
    username = fields.CharField(max_length=32, null=True)
    status = fields.CharField(max_length=32, null=True)  # manager
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @classmethod
    async def update_data(cls, user_id: int, username: str):
        user = await cls.filter(user_id=user_id).first()
        if user is None:
            await cls.create(
                user_id=user_id,
                username=username,
            )
        else:
            await cls.filter(user_id=user_id).update(
                username=username,
                updated_at=datetime.now(),
            )

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


class Request(Model):
    class Meta:
        table = 'requests'
        ordering = ['created_at']

    class RequestType(Enum):
        calculator = 'calculator'
        manager_support = 'manager_support'

    id = fields.CharField(max_length=8, pk=True)
    user = fields.ForeignKeyField('models.User', to_field='user_id', related_name='requests_user')
    type = fields.CharEnumField(enum_type=RequestType, max_length=64, null=True)

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
            type=type,
            calculator_data=calculator_data,
            calculator_photo=calculator_photo,
            support_data=support_data,
        )
        return request


class RequestLog(Model):
    class Meta:
        table = 'request_logs'
        ordering = ['id']

    id = fields.BigIntField(pk=True)
    request = fields.ForeignKeyField('models.Request', to_field='id')
    manager = fields.ForeignKeyField('models.User', to_field='user_id')


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
