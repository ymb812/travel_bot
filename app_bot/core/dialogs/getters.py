from aiogram.enums import ContentType
from core.database.models import User, Post
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from settings import settings


async def get_main_menu_content(dialog_manager: DialogManager, **kwargs):
    post_id = None
    if 'info' in dialog_manager.event.data:
        post_id = settings.info_post_id
    elif 'socials' in dialog_manager.event.data:
        post_id = settings.socials_post_id
    elif 'addresses' in dialog_manager.event.data:
        post_id = settings.addresses_post_id
    elif 'payment_data' in dialog_manager.event.data:
        post_id = settings.payment_data_post_id

    elif 'delivery' in dialog_manager.event.data:
        post_id = settings.delivery_post_id
    elif 'requirements' in dialog_manager.event.data:
        post_id = settings.requirements_post_id
    elif 'poizon' in dialog_manager.event.data:
        post_id = settings.poizon_post_id
    elif 'contract' in dialog_manager.event.data:
        post_id = settings.contract_post_id

    elif 'cases' in dialog_manager.event.data:
        post_id = settings.cases_post_id

    elif 'reviews' in dialog_manager.event.data:
        post_id = settings.reviews_post_id

    elif 'currency' in dialog_manager.event.data:
        post_id = settings.currency_post_id



    post = await Post.get(id=post_id)
    media_content = None
    if post.document_file_id:
        media_content = MediaAttachment(ContentType.DOCUMENT, url=post.document_file_id)
    elif post.video_file_id:
        media_content = MediaAttachment(ContentType.VIDEO, url=post.video_file_id)
    elif post.photo_file_id:
        media_content = MediaAttachment(ContentType.PHOTO, url=post.photo_file_id)

    return {
        'msg_text': post.text,
        'media_content': media_content,
    }


async def get_bot_data(dialog_manager: DialogManager, **kwargs):
    return {
        'bot_username': (await dialog_manager.event.bot.get_me()).username
    }
