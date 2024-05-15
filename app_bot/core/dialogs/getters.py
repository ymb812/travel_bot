from aiogram.enums import ContentType
from core.database.models import User, UserLog, FAQ, Post, ManagerCard
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from core.dialogs.callbacks import get_username_or_link
from settings import settings


async def get_main_menu_content(dialog_manager: DialogManager, **kwargs):
    # add info about User's state
    state = dialog_manager.event.data.split('')[-1]

    await UserLog.create_log(user_id=dialog_manager.event.from_user.id, state=state)

    post_id = None
    if 'info' in dialog_manager.event.data:  # useless cuz of new window
        post_id = settings.info_post_id
    elif 'socials' in dialog_manager.event.data:  # useless cuz of new window
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
    elif 'alipay' in dialog_manager.event.data:
        post_id = settings.alipay_post_id
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


async def get_managers_cards(dialog_manager: DialogManager, **kwargs):
    current_page = await dialog_manager.find('manager_card_scroll').get_page()
    managers_cards = await ManagerCard.all().order_by('order_priority')
    current_card = managers_cards[current_page]

    # data for CallbackHandler
    if managers_cards:
        dialog_manager.dialog_data['pages'] = len(managers_cards)
    else:
        raise ValueError

    media_content = MediaAttachment(ContentType.PHOTO, url=current_card.photo)
    msg_text = f'<b>{current_card.name}</b>\n\n' \
               f'{current_card.description}'

    return {
        'media_content': media_content,
        'msg_text': msg_text,
        'pages': len(managers_cards),
        'current_page': current_page + 1,
    }


async def get_question(dialog_manager: DialogManager, **kwargs):
    question = await FAQ.get(id=dialog_manager.dialog_data['question_id'])
    media_content = MediaAttachment(ContentType.VIDEO, url=question.video_file_id)

    return {
        'media_content': media_content,
    }


async def get_statuses(**kwargs) -> dict[str]:
    statuses_dict = {status.name: status.value for status in User.StatusType}
    statuses = [status for status in User.StatusType if status.value not in ['admin', 'manager']]

    return {
        'statuses': statuses,
        'statuses_dict': statuses_dict,
    }


async def get_users_by_manager(dialog_manager: DialogManager, **kwargs) -> dict[str, list[User]]:
    current_page = await dialog_manager.find('user_scroll').get_page()
    users = await User.filter(
        manager_id=dialog_manager.event.from_user.id,
        status=dialog_manager.dialog_data['filter_by_status'],
    )
    if len(users) == 1:
        current_page = 0  # bypass error if we dynamically delete page
    current_user = users[current_page]

    # data for CallbackHandler
    if users:
        dialog_manager.dialog_data['pages'] = len(users)
    dialog_manager.dialog_data['current_user_user_id'] = current_user.user_id
    dialog_manager.dialog_data['statuses_dict'] = (await get_statuses(**kwargs))['statuses_dict']
    username = get_username_or_link(user=current_user)

    return {
        'pages': len(users),
        'current_page': current_page + 1,
        'username': username,
        'user_status': current_user.status,
        'statuses': (await get_statuses(**kwargs))['statuses'],
    }
