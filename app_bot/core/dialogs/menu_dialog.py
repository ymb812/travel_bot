from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.common.scroll import sync_scroll
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.kbd import PrevPage, NextPage, CurrentPage, Start, Column, StubScroll, Button, Row, \
    FirstPage, LastPage, Select, SwitchTo, Url
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _
from core.dialogs.custom_content import CustomPager, Multicolumn
from core.dialogs.callbacks import MainMenuCallbackHandler
from core.dialogs.getters import get_main_menu_content, get_questions, get_question, get_managers_cards,\
    get_addresses_content, get_cases, get_case, get_warehouse_video
from settings import settings


main_menu_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            SwitchTo(Const(text='О компании Чайна Тревел'), id='go_to_info', state=MainMenuStateGroup.pick_info),
            SwitchTo(Const(text='Отзывы'), id='go_to_reviews', state=MainMenuStateGroup.reviews),
            SwitchTo(Const(text='Кейсы клиентов'), id='go_to_cases', state=MainMenuStateGroup.pick_case),
            SwitchTo(Const(text='Актуальный курс юаня'), id='go_to_currency', state=MainMenuStateGroup.currency),
            SwitchTo(Const(text='Условия работы'), id='go_to_requirements', state=MainMenuStateGroup.pick_requirements),
            SwitchTo(Const(text='Видео ответы на частые вопросы'), id='go_to_faq', state=MainMenuStateGroup.pick_faq),
            SwitchTo(Const(text='Калькулятор доставки'), id='go_to_calculator', state=MainMenuStateGroup.input_length),
            Button(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', on_click=MainMenuCallbackHandler.start_manager_support),
            Url(Const(text='Если у вас есть жалобы, напишите нам'), id='url_', url=Const('https://t.me/MG3_ChTr')),
        ),
        state=MainMenuStateGroup.menu,
    ),

    # pick info
    Window(
        Const(text=_('О компании «чайна Тревел». Выберите действие ⤵️')),
        SwitchTo(Const(text='Обзор нашего склада'), id='info', state=MainMenuStateGroup.warehouse),
        SwitchTo(Const(text='Соц.сети'), id='socials', state=MainMenuStateGroup.socials),
        SwitchTo(Const(text='Наши адреса'), id='addresses', state=MainMenuStateGroup.addresses),
        SwitchTo(Const(text='Реквизиты компании'), id='payment_data', state=MainMenuStateGroup.info),
        Button(Const(text='Сотрудники China Trevel'), id='go_to_managers', on_click=MainMenuCallbackHandler.open_managers_cards),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.pick_info
    ),

    # warehouse
    Window(
        Const(text='Обзор нашего склада. Выберите действие ⤵️'),
        Url(Const(text='Прямая трансляция'), id='url_warehouse', url=Const('https://t.me/china_travel_ru/865')),
        Url(Const(text='Ссылка на фотографии'), id='url_telegraph', url=Const('https://telegra.ph/China-Trevel-05-16')),
        SwitchTo(Const(text='Видео 1'), id='warehouse_video_1', state=MainMenuStateGroup.warehouse_video),
        SwitchTo(Const(text='Видео 2'), id='warehouse_video_2', state=MainMenuStateGroup.warehouse_video),
        SwitchTo(Const(text='Видео 3'), id='warehouse_video_3', state=MainMenuStateGroup.warehouse_video),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_info', state=MainMenuStateGroup.pick_info),
        state=MainMenuStateGroup.warehouse
    ),

    # warehouse_video
    Window(
        DynamicMedia(selector='media_content'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_warehouse', state=MainMenuStateGroup.warehouse),
        getter=get_warehouse_video,
        state=MainMenuStateGroup.warehouse_video
    ),

    # addresses
    Window(
        Const(text='Наши адреса'),
        SwitchTo(Const(text='Китай, Фошань'), id='address_foshan_1', state=MainMenuStateGroup.addresses_info),
        SwitchTo(Const(text='Китай, Фошань'), id='address_foshan_2', state=MainMenuStateGroup.addresses_info),
        SwitchTo(Const(text='Китай, Пекин'), id='address_pekin', state=MainMenuStateGroup.addresses_info),
        SwitchTo(Const(text='Китай, Иу'), id='address_iu', state=MainMenuStateGroup.addresses_info),
        SwitchTo(Const(text='Россия, Люблено'), id='address_russia_1', state=MainMenuStateGroup.addresses_info),
        SwitchTo(Const(text='Россия, Южные Ворота'), id='address_russia_2', state=MainMenuStateGroup.addresses_info),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_info', state=MainMenuStateGroup.pick_info),
        state=MainMenuStateGroup.addresses
    ),

    # addresses_info
    Window(
        Format(text='{msg_text}'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_addresses', state=MainMenuStateGroup.addresses),
        getter=get_addresses_content,
        state=MainMenuStateGroup.addresses_info
    ),

    # socials
    Window(
        Const(text='Наши соц. сети 👇'),
        Url(Const(text='Telegram'), id='url_tg', url=Const('https://t.me/MG3_ChTr')),
        Url(Const(text='Instagram'), id='url_inst', url=Const('https://instagram.com/china__trevel?igshid=YmMyMTA2M2Y=')),
        Url(Const(text='ВКонтакте'), id='url_vk', url=Const('https://vk.com/chinatrevel')),
        Url(Const(text='Сайт'), id='url_vk', url=Const('https://chinatravel-tk.ru/')),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_info', state=MainMenuStateGroup.pick_info),
        state=MainMenuStateGroup.socials
    ),

    # reviews
    Window(
        Const(text='Наши отзывы'),
        Url(Const(text='Фото отзывы'), id='url_tg_photo', url=Const('https://t.me/MG3_ChTr')),
        Url(Const(text='Видео отзывы'), id='url_tg_video', url=Const('https://t.me/MG3_ChTr')),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.reviews
    ),

    # info
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_info', state=MainMenuStateGroup.pick_info),
        getter=get_main_menu_content,
        state=MainMenuStateGroup.info
    ),

    # managers_cards
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        StubScroll(id='manager_card_scroll', pages='pages'),

        # cycle pager
        Row(
            LastPage(scroll='manager_card_scroll', text=Const('<'), when=F['current_page'] == 0),
            PrevPage(scroll='manager_card_scroll', when=F['current_page'] != 0),
            CurrentPage(scroll='manager_card_scroll'),
            NextPage(scroll='manager_card_scroll', when=F['current_page'] != F['pages'] - 1),
            FirstPage(scroll='manager_card_scroll', text=Const('>'), when=F['current_page'] == F['pages'] - 1),
            when=F['pages'] > 1,
        ),

        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_managers_cards,
        state=MainMenuStateGroup.managers_cards,
    ),

    # pick requirements
    Window(
        Const(text=_('PICK_ACTION')),
        SwitchTo(Const(text='Доставка и ее стоимость'), id='delivery', state=MainMenuStateGroup.requirements),
        SwitchTo(Const(text='Условия по выкупу'), id='requirements', state=MainMenuStateGroup.requirements),
        SwitchTo(Const(text='Poizon'), id='poizon', state=MainMenuStateGroup.requirements),
        SwitchTo(Const(text='Alipay'), id='alipay', state=MainMenuStateGroup.requirements),
        SwitchTo(Const(text='Шаблон договора'), id='contract', state=MainMenuStateGroup.requirements),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.pick_requirements
    ),

    # requirements
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_requirements', state=MainMenuStateGroup.pick_requirements),
        getter=get_main_menu_content,
        state=MainMenuStateGroup.requirements
    ),

    # currency
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_main_menu_content,
        state=MainMenuStateGroup.currency
    ),

    # pick_case
    Window(
        Const(text='Наши кейсы'),
        CustomPager(
            Multicolumn(
                Select(
                    id='_cases_odd_select',
                    items='cases_odd',
                    item_id_getter=lambda item: item.id,
                    text=Format(text='Кейс {item.order_priority}'),
                    on_click=MainMenuCallbackHandler.selected_case,
                ),
                Select(
                    id='_cases_even_select',
                    items='cases_even',
                    item_id_getter=lambda item: item.id,
                    text=Format(text='Кейс {item.order_priority}'),
                    on_click=MainMenuCallbackHandler.selected_case,
                ),
            ),
            id='case_group',
            height=5,
            width=2,
            hide_on_single_page=True,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_cases,
        state=MainMenuStateGroup.pick_case
    ),

    # case
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_cases', state=MainMenuStateGroup.pick_case),
        getter=get_case,
        state=MainMenuStateGroup.case
    ),


    # pick faq - scroll text and buttons
    Window(
        List(
            Format(text='{item}'),
            items='questions_texts',
            id='questions_text_scroll',
            page_size=settings.faq_per_page_height,
        ),
        CustomPager(
            Select(
                id='_question_select',
                items='questions',
                item_id_getter=lambda item: item.id,
                text=Format(text='Вопрос {item.order_priority}'),
                on_click=MainMenuCallbackHandler.selected_product,
            ),
            id='question_group',
            height=settings.faq_per_page_height,
            width=settings.faq_per_page_width,
            on_page_changed=sync_scroll(scroll_id='questions_text_scroll'),
            hide_on_single_page=True,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_questions,
        state=MainMenuStateGroup.pick_faq
    ),

    # faq
    Window(
        DynamicMedia(selector='media_content'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_faq', state=MainMenuStateGroup.pick_faq),
        getter=get_question,
        state=MainMenuStateGroup.faq
    ),



    # calculator_data input_length
    Window(
        Const(text=_('INPUT_CALCULATOR_DATA')),
        TextInput(
            id='input_length',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        Button(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', on_click=MainMenuCallbackHandler.start_manager_support),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.input_length
    ),

    # input_width
    Window(
        Const(text='Введите ширину'),
        TextInput(
            id='input_width',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_length', state=MainMenuStateGroup.input_length),
        state=MainMenuStateGroup.input_width,
    ),

    # input_height
    Window(
        Const(text='Введите высоту'),
        TextInput(
            id='input_height',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_width', state=MainMenuStateGroup.input_width),
        state=MainMenuStateGroup.input_height,
    ),

    # input_photo
    Window(
        Const(text=_('Финальный шаг - прикрепите фото (не обязательно)')),
        MessageInput(
            func=MainMenuCallbackHandler.entered_calculator_photo,
            content_types=[ContentType.PHOTO],
        ),
        Button(Const(text='Пропустить и отправить данные'), id='send_new_request', on_click=MainMenuCallbackHandler.create_new_request),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_heigth', state=MainMenuStateGroup.input_height),
        state=MainMenuStateGroup.input_photo
    ),
)
