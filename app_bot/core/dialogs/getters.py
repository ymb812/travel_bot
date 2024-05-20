from aiogram.enums import ContentType
from core.database.models import User, UserLog, FAQ, Post, ManagerCard, Case, Currency
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

    elif 'requirements' in dialog_manager.event.data:
        post_id = settings.requirements_post_id
    elif 'poizon' in dialog_manager.event.data:
        post_id = settings.poizon_post_id
    elif 'alipay' in dialog_manager.event.data:
        post_id = settings.alipay_post_id
    elif 'contract_fiz' in dialog_manager.event.data:
        post_id = settings.contract_post_id
    elif 'contract_ur' in dialog_manager.event.data:
        post_id = 114

    elif 'pick_case' in dialog_manager.event.data:
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


async def get_warehouse_video(dialog_manager: DialogManager, **kwargs):
    if 'warehouse_video_1' in dialog_manager.event.data:  # useless cuz of new window
        post_id = 1001
    elif 'warehouse_video_2' in dialog_manager.event.data:  # useless cuz of new window
        post_id = 1002
    elif 'warehouse_video_3' in dialog_manager.event.data:
        post_id = 1003

    post = await Post.get(id=post_id)
    media_content = MediaAttachment(ContentType.VIDEO, url=post.video_file_id)

    return {
        'media_content': media_content,
    }


async def get_delivery_files(dialog_manager: DialogManager, **kwargs):
    if 'delivery_1' in dialog_manager.event.data:
        post_id = 2001
    elif 'delivery_2' in dialog_manager.event.data:
        post_id = 2002
    elif 'delivery_3' in dialog_manager.event.data:
        post_id = 2003
    elif 'delivery_4' in dialog_manager.event.data:
        post_id = 2004

    post = await Post.get(id=post_id)
    media_content = MediaAttachment(ContentType.DOCUMENT, url=post.document_file_id)

    return {
        'msg_text': post.text,
        'media_content': media_content,
    }


async def get_addresses_content(dialog_manager: DialogManager, **kwargs):
    if 'address_foshan_1' in dialog_manager.event.data:
        msg_text = '''Фошань 

收货人: 王洪威
手机号码: 18520718666
 广东省佛山市南海区里水镇
流潮村共同1号之二

Адрес Фошань  на английском языке：
2 zhi，1- gongtong，liuchaocun,Lishui Town， Nanhai District ， foshan city,  China
получителя :Wanghongwei
телефон: +8618520718666
Почтовый индекс: （528244）'''

    elif 'address_foshan_2' in dialog_manager.event.data:
        msg_text = '''Фошань 

收货人: 孟亚文
手机号码: 17786857118
 广东省佛山市南海区里水镇
流潮村共同1号之三

3 zhi，1- gongtong，liuchaocun,Lishui Town， Nanhai District ， foshan city,  China
получителя :Mengyawen
телефон: +86
Почтовый индекс: 528244'''

    elif 'address_pekin' in dialog_manager.event.data:
        msg_text = '''Пекин:

北京市朝阳区日坛北路日坛国际贸易中心B座118A-288A库房
戈启东18733716378

На английском
Warehouse 118A-288A, Building B, Ritan International Trade Center, Ritan North Road, Chaoyang District, Beijing
Ge Qidong 18733716378'''

    elif 'address_iu' in dialog_manager.event.data:
        msg_text = '''Иу:

戈启东18520718666
浙江省 金华市 义乌市
北苑街道川塘路8号 118A 库房

На английском 
Ge Qidong 18520718666
Yiwu City, Jinhua City, Zhejiang Province
Warehouse 118A, No. 8 Chuantang Road, Beiyuan Street'''

    elif 'address_russia_1' in dialog_manager.event.data:
        msg_text = '''Люблено 

Москва, ТЯК Люблино, Тихорецкий бульвар дом 1 (вход- 7 и 7А).'''

    elif 'address_russia_2' in dialog_manager.event.data:
        msg_text = '''Южные Ворота          
                
Москва, Южные ворота, МКАД 19 км. Вход 15 напротив карго "Сбор грузов".'''

    return {
        'msg_text': msg_text,
    }


async def get_cases(dialog_manager: DialogManager, **kwargs):
    cases = await Case.all().order_by('order_priority')
    cases_even = [case for case in cases if case.id % 2 == 0]
    cases_odd = [case for case in cases if case.id % 2 != 0]

    return {
        'cases_even': cases_even,
        'cases_odd': cases_odd,
    }


async def get_case(dialog_manager: DialogManager, **kwargs):
    case = await Case.get(id=dialog_manager.dialog_data['case_id'])
    media_content = None
    if case.photo_file_id:
        media_content = MediaAttachment(ContentType.PHOTO, url=case.photo_file_id)

    msg_text = f'<b>{case.name}</b>\n\n' \
               f'{case.description}'

    return {
        'msg_text': msg_text,
        'media_content': media_content,
    }


async def get_questions(dialog_manager: DialogManager, **kwargs):
    questions = await FAQ.all().order_by('order_priority')
    questions_texts = []
    for question in questions:
        questions_texts.append(f'{question.order_priority}. {question.question}\n')
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


async def get_statuses(**kwargs) -> dict[str]:
    statuses_dict = {status.name: status.value for status in User.StatusType}
    statuses = [status for status in User.StatusType if status.value not in ['admin', 'manager']]
    statuses_for_filter = [status for status in User.StatusType if status.value not in ['admin', 'manager', 'Реализован', 'Не реализован']]

    return {
        'statuses': statuses,
        'statuses_dict': statuses_dict,
        'statuses_for_filter': statuses_for_filter,
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


async def get_currency(dialog_manager: DialogManager, **kwargs):
    currency = await Currency.first()

    return {
        'currency': currency.currency,
    }
