from aiogram.enums import ContentType
from core.database.models import User, FAQ, Post
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


async def get_questions(dialog_manager: DialogManager, **kwargs):
    questions = await FAQ.all().order_by('order_priority')
    questions_texts = ''
    for question in questions:
        questions_texts += f'{question.order_priority}. {question.question}\n\n'

    return {
        'questions': questions,
        'questions_texts': questions_texts,
    }


async def get_question(dialog_manager: DialogManager, **kwargs):
    question = await FAQ.get(id=dialog_manager.dialog_data['question_id'])
    media_content = MediaAttachment(ContentType.VIDEO, url=question.video_file_id)

    return {
        'media_content': media_content,
    }
