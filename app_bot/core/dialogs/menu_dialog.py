from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Url, SwitchTo, Button, Start, Select
from core.states.main_menu import MainMenuStateGroup
from core.states.calculator import CalculatorStateGroup
from core.states.manager_support import ManagerSupportStateGroup
from core.utils.texts import _
from core.dialogs.custom_content import CustomPager
from core.dialogs.callbacks import MainMenuCallbackHandler
from core.dialogs.getters import get_main_menu_content, get_questions, get_question
from settings import settings


main_menu_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            SwitchTo(Const(text='О компании Чайна Тревел'), id='go_to_info', state=MainMenuStateGroup.pick_info),
            SwitchTo(Const(text='Условия работы'), id='go_to_requirements', state=MainMenuStateGroup.pick_requirements),
            SwitchTo(Const(text='FAQ'), id='go_to_faq', state=MainMenuStateGroup.pick_faq),
            SwitchTo(Const(text='Кейсы клиентов'), id='go_to_cases', state=MainMenuStateGroup.cases_reviews_currency),
            SwitchTo(Const(text='Отзывы'), id='go_to_reviews', state=MainMenuStateGroup.cases_reviews_currency),
            SwitchTo(Const(text='Актуальный курс юаня'), id='go_to_currency', state=MainMenuStateGroup.cases_reviews_currency),
            SwitchTo(Const(text='Калькулятор доставки'), id='go_to_calculator', state=MainMenuStateGroup.pick_calculator),
            Start(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', state=ManagerSupportStateGroup.input_fio),
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

    # calculator_data input
    Window(
        Const(text=_('INPUT_CALCULATOR_DATA')),
        MessageInput(
            func=MainMenuCallbackHandler.entered_calculator_data,
            content_types=[ContentType.TEXT, ContentType.PHOTO]
        ),
        Start(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', state=ManagerSupportStateGroup.input_fio),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        state=MainMenuStateGroup.pick_calculator
    ),
)
