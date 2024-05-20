from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Button, Start
from core.states.main_menu import MainMenuStateGroup
from core.states.manager_support import ManagerSupportStateGroup
from core.utils.texts import _
from core.dialogs.callbacks import ManagerSupportCallbackHandler


manager_support_dialog = Dialog(
    # input fio
    Window(
        Const(text=_('INPUT_FIO')),
        TextInput(
            id='input_fio',
            type_factory=str,
            on_success=ManagerSupportCallbackHandler.entered_fio
        ),
        Start(Const(text=_('BACK_BUTTON')), id='switch_to_floor', state=MainMenuStateGroup.menu),
        state=ManagerSupportStateGroup.input_fio,
    ),


    # sell_and_delivery
    Window(
        Const(text='Вас интересует выкуп или доставка'),
        Column(
            Button(Const(text='Выкуп'), id='sell', on_click=ManagerSupportCallbackHandler.entered_sell_and_delivery),
            Button(Const(text='Доставка'), id='pick_delivery', on_click=ManagerSupportCallbackHandler.entered_sell_and_delivery),
            Button(Const(text='Все сразу'), id='sell_and_delivery', on_click=ManagerSupportCallbackHandler.entered_sell_and_delivery),
            SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_fio', state=ManagerSupportStateGroup.input_fio),
        ),
        state=ManagerSupportStateGroup.sell_and_delivery,
    ),

    # did_work
    Window(
        Const(text='Ранее вы уже работали с карго?'),
        Column(
            Button(Const(text='Да'), id='did_work', on_click=ManagerSupportCallbackHandler.entered_did_work),
            Button(Const(text='Нет'), id='did_not_work', on_click=ManagerSupportCallbackHandler.entered_did_work),
            SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_s_and_d', state=ManagerSupportStateGroup.sell_and_delivery),
        ),
        state=ManagerSupportStateGroup.did_work,
    ),

    # from_where
    Window(
        Const(text='Как Вы о нас узнали?'),
        Column(
            Button(Const(text='Рекомендация знакомых'), id='friends', on_click=ManagerSupportCallbackHandler.entered_sell_and_delivery),
            Button(Const(text='Узнал от блогеров'), id='blogers', on_click=ManagerSupportCallbackHandler.entered_from_where),
            Button(Const(text='Вконтакте'), id='vkonakte', on_click=ManagerSupportCallbackHandler.entered_from_where),
            Button(Const(text='Telegram'), id='telegram', on_click=ManagerSupportCallbackHandler.entered_from_where),
            Button(Const(text='Авито'), id='avito', on_click=ManagerSupportCallbackHandler.entered_from_where),
            Button(Const(text='Сайт'), id='site', on_click=ManagerSupportCallbackHandler.entered_from_where),
            SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_did_work', state=ManagerSupportStateGroup.did_work),
        ),
        state=ManagerSupportStateGroup.from_where,
    ),
)
