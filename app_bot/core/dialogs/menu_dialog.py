from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Url, SwitchTo, Button, Start
from core.states.main_menu import MainMenuStateGroup
from core.states.calculator import CalculatorStateGroup
from core.states.manager import ManagerStateGroup
from core.utils.texts import _
from core.dialogs.callbacks import MainMenuCallbackHandler
from core.dialogs.getters import get_main_menu_content
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
            Start(Const(text='Калькулятор доставки'), id='go_to_calculator', state=CalculatorStateGroup.menu),
            Start(Const(text='Связаться с менеджером для заказа'), id='go_to_manager', state=ManagerStateGroup.input_fio),
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
)
