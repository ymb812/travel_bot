from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import PrevPage, NextPage, CurrentPage, Start, Column, StubScroll, Button, Row, \
    FirstPage, LastPage, Select
from core.dialogs.getters import get_statuses, get_users_by_manager
from core.dialogs.callbacks import ManagerCallbackHandler
from core.states.manager import ManagerStateGroup
from core.utils.texts import _


manager_dialog = Dialog(
    # manager_menu
    Window(
        Format(text='Выберите статус, по которому отобразить список пользователей'),
        Column(
            Select(
                id='_status_select',
                items='statuses',
                item_id_getter=lambda item: item.value,
                text=Format(text='{item.value}'),
                on_click=ManagerCallbackHandler.selected_status,
            ),
        ),
        getter=get_statuses,
        state=ManagerStateGroup.manager_menu
    ),

    # users_list
    Window(
        Format(text='Пользователь: {username}\nТекущий статус: {user_status}'),
        StubScroll(id='user_scroll', pages='pages'),

        # cycle pager
        Row(
            LastPage(scroll='user_scroll', text=Const('<'), when=F['current_page'] == 0),
            PrevPage(scroll='user_scroll', when=F['current_page'] != 0),
            CurrentPage(scroll='user_scroll'),
            NextPage(scroll='user_scroll', when=F['current_page'] != F['pages'] - 1),
            FirstPage(scroll='user_scroll', text=Const('>'), when=F['current_page'] == F['pages'] - 1),
            when=F['pages'] > 1,
        ),

        Column(
            Select(
                id='_status_select',
                items='statuses',
                item_id_getter=lambda item: item.name,
                text=Format(text='{item.value}'),
                on_click=ManagerCallbackHandler.change_user_status,
            ),
            Start(Const(text=_('BACK_BUTTON')), id='go_to_manager_menu', state=ManagerStateGroup.manager_menu)
        ),
        getter=get_users_by_manager,
        state=ManagerStateGroup.users_list,
    ),
)
