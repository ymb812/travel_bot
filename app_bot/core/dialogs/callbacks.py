import logging
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.calculator import CalculatorStateGroup
from core.states.main_menu import MainMenuStateGroup
from core.states.manager_support import ManagerSupportStateGroup
from core.database.models import User, Request, Post
from core.utils.texts import _
from broadcaster import Broadcaster
from settings import settings


logger = logging.getLogger(__name__)


class MainMenuCallbackHandler:
    @classmethod
    async def selected_product(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        dialog_manager.dialog_data['question_id'] = item_id
        await dialog_manager.switch_to(MainMenuStateGroup.faq)


    # create new calculator request
    @staticmethod
    async def entered_calculator_data(
            message: Message,
            widget: MessageInput,
            dialog_manager: DialogManager,
    ):
        calculator_photo = None
        if message.photo:
            calculator_photo = message.photo[-1].file_id

        request = await Request.create_request(
            user_id=message.from_user.id,
            type=Request.RequestType.calculator,
            calculator_data=message.text,
            calculator_photo=calculator_photo,
        )

        await message.answer(text=_('REQUEST_INFO', request_id=request.id))
        await dialog_manager.switch_to(MainMenuStateGroup.menu)


    @classmethod
    async def main_menu_content(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        pass


class ManagerSupportCallbackHandler:
    @staticmethod
    async def entered_fio(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value: str,
    ):
        dialog_manager.dialog_data['fio'] = value
        await dialog_manager.switch_to(ManagerSupportStateGroup.sell_and_delivery)


    @staticmethod
    async def entered_sell_and_delivery(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        if callback.data == 'sell':
            value = 'Выкуп'

        elif callback.data == 'delivery':
            value = 'Доставка'

        elif callback.data == 'sell_and_delivery':
            value = 'Все сразу'

        dialog_manager.dialog_data['sell_and_delivery'] = f'Вас интересует выкуп или доставка товаров?\n' \
                                                          f'{value}\n\n'
        await dialog_manager.switch_to(ManagerSupportStateGroup.did_work)


    @staticmethod
    async def entered_did_work(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        if callback.data == 'did_work':
            value = 'Да'

        elif callback.data == 'did_not_work':
            value = 'Нет'

        dialog_manager.dialog_data['did_work'] = f'Ранее вы уже работали с карго?\n' \
                                                 f'{value}\n\n'
        await dialog_manager.switch_to(ManagerSupportStateGroup.from_where)


    @staticmethod
    async def entered_from_where(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        if callback.data == 'friends':
            value = 'Рекомендация знакомых'

        elif callback.data == 'blogers':
            value = 'Узнал от блогеров'

        elif callback.data == 'vkonakte':
            value = 'Вконтакте'

        elif callback.data == 'telegram':
            value = 'Telegram'

        elif callback.data == 'avito':
            value = 'Авито'

        elif callback.data == 'site':
            value = 'Сайт'

        dialog_manager.dialog_data['from_where'] = f'Как Вы о нас узнали?\n' \
                                                   f'{value}\n\n'

        # update user fio
        await User.filter(user_id=callback.from_user.id).update(
            fio=dialog_manager.dialog_data['fio'],
        )

        # create new request and send to manager
        support_data = \
            dialog_manager.dialog_data['sell_and_delivery']\
            + dialog_manager.dialog_data['did_work']\
            + dialog_manager.dialog_data['from_where']
        request = await Request.create_request(
            user_id=callback.from_user.id,
            type=Request.RequestType.manager_support,
            support_data=support_data,
        )

        await callback.message.answer(text=_('REQUEST_INFO', request_id=request.id))
        await dialog_manager.start(MainMenuStateGroup.menu)
