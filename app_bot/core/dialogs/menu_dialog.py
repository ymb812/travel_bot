from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import PrevPage, NextPage, CurrentPage, Start, Column, StubScroll, Button, Row, \
    FirstPage, LastPage, Select, SwitchTo
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _
from core.dialogs.custom_content import CustomPager
from core.dialogs.callbacks import MainMenuCallbackHandler
from core.dialogs.getters import get_main_menu_content, get_questions, get_question, get_managers_cards
from settings import settings


main_menu_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            SwitchTo(Const(text='О компании Чайна Тревел'), id='go_to_info', state=MainMenuStateGroup.pick_info),
            SwitchTo(Const(text='Условия работы'), id='go_to_requirements', state=MainMenuStateGroup.pick_requirements),
            SwitchTo(Const(text='Видео ответы на частые вопросы'), id='go_to_faq', state=MainMenuStateGroup.pick_faq),
            SwitchTo(Const(text='Кейсы клиентов'), id='go_to_cases', state=MainMenuStateGroup.cases_reviews_currency),
            SwitchTo(Const(text='Отзывы'), id='go_to_reviews', state=MainMenuStateGroup.cases_reviews_currency),
            SwitchTo(Const(text='Актуальный курс юаня'), id='go_to_currency', state=MainMenuStateGroup.cases_reviews_currency),
            SwitchTo(Const(text='Калькулятор доставки'), id='go_to_calculator', state=MainMenuStateGroup.input_photo),
            Button(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', on_click=MainMenuCallbackHandler.start_manager_support),
        ),
        state=MainMenuStateGroup.menu,
    ),

    # pick info
    Window(
        Const(text=_('PICK_ACTION')),
        SwitchTo(Const(text='Обзор нашего склада'), id='info', state=MainMenuStateGroup.info),
        SwitchTo(Const(text='Соц.сети'), id='socials', state=MainMenuStateGroup.info),
        SwitchTo(Const(text='Наши адреса'), id='addresses', state=MainMenuStateGroup.info),
        SwitchTo(Const(text='Реквизиты компании'), id='payment_data', state=MainMenuStateGroup.info),
        Button(Const(text='Наши менеджеры'), id='go_to_managers', on_click=MainMenuCallbackHandler.open_managers_cards),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.pick_info
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

    # cases / reviews / currency
    Window(
        DynamicMedia(selector='media_content'),
        Format(text='{msg_text}'),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_main_menu_content,
        state=MainMenuStateGroup.cases_reviews_currency
    ),

    # pick faq
    Window(
        Format(text='{questions_texts}'),
        CustomPager(
            Select(
                id='_question_select',
                items='questions',
                item_id_getter=lambda item: item.id,
                text=Format(text='Вопрос {item.order_priority}'),
                on_click=MainMenuCallbackHandler.selected_product,
            ),
            id='question_group',
            height=settings.categories_per_page_height,
            width=settings.categories_per_page_width,
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

    # calculator_data input_photo
    Window(
        Const(text=_('INPUT_CALCULATOR_DATA')),
        MessageInput(
            func=MainMenuCallbackHandler.entered_calculator_photo,
            content_types=[ContentType.PHOTO],
        ),
        Button(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', on_click=MainMenuCallbackHandler.start_manager_support),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.input_photo
    ),

    # input_volume
    Window(
        Const(text='Введите объем'),
        TextInput(
            id='input_volume',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_photo', state=MainMenuStateGroup.input_photo),
        state=MainMenuStateGroup.input_volume,
    ),

    # input_width
    Window(
        Const(text='Введите ширину'),
        TextInput(
            id='input_width',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_volume', state=MainMenuStateGroup.input_volume),
        state=MainMenuStateGroup.input_width,
    ),

    # input_density
    Window(
        Const(text='Введите плотность'),
        TextInput(
            id='input_density',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_width', state=MainMenuStateGroup.input_width),
        state=MainMenuStateGroup.input_density,
    ),

    # input_weight
    Window(
        Const(text='Введите вес'),
        TextInput(
            id='input_weight',
            type_factory=str,
            on_success=MainMenuCallbackHandler.entered_calculator_text_data,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_density', state=MainMenuStateGroup.input_density),
        state=MainMenuStateGroup.input_weight,
    ),
)
