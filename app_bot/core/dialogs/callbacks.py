import logging
import string
import random
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.main_menu import MainMenuStateGroup
from core.states.manager_support import ManagerSupportStateGroup
from core.database.models import User, Request, RequestLog
from core.keyboards.inline import add_comment_kb
from core.utils.texts import _
from broadcaster import Broadcaster
from settings import settings


logger = logging.getLogger(__name__)


def generate_random_string(length: int = 8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_username_or_link(user: User):
    if user.username:
        user_username = f'@{user.username}'
    else:
        user_username = f'<a href="tg://user?id={user.user_id}">ссылка</a>'

    return user_username


async def send_new_request(request: Request, bot: Bot):
    managers = await User.filter(status='manager').all().order_by('id')
    logs = await RequestLog.all().order_by('id')
    if not managers:
        return

    manager_to_send: User = managers[0]
    if logs:
        last_manager: User = await logs[-1].manager
        try:
            manager_to_send = managers[managers.index(last_manager) + 1]
        except IndexError:
            logger.info(f'Going to the 1st manager_id={manager_to_send.user_id}')
        except ValueError:
            logger.error(f'There is no manager manager_id={manager_to_send.user_id}')

    # send request (calculator/support)
    user: User = await request.user
    if request.type == request.RequestType.calculator.value:
        type = 'калькулятор доставки'
        data = request.calculator_data

    elif request.type == request.RequestType.manager_support.value:
        type = 'связь с менеджером'
        data = request.support_data

    fio = ''
    if user.fio:
        fio = f'ФИО: {user.fio}\n'

    if request.calculator_photo:
        await bot.send_photo(
            chat_id=manager_to_send.user_id,
            photo=request.calculator_photo,
            caption=_(
                text='REQUEST_TEXT',
                request_id=request.id,
                type=type,
                username=get_username_or_link(user=await request.user),
                fio=fio,
                data=data,
                    ),
            reply_markup=add_comment_kb(request_id=request.id),
        )

    else:
        await bot.send_message(
            chat_id=manager_to_send.user_id,
            text=_(
                text='REQUEST_TEXT',
                request_id=request.id,
                type=type,
                username=get_username_or_link(user),
                fio=fio,
                data=data,
                    ),
            reply_markup=add_comment_kb(request_id=request.id),
        )

    # add log and add manager to request
    await RequestLog.create(request_id=request.id, manager_id=manager_to_send.user_id)
    request.manager_id = manager_to_send.user_id
    await request.save()


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
        calculator_data = message.text
        calculator_photo = None
        if message.photo:
            calculator_data = message.caption
            calculator_photo = message.photo[-1].file_id

        request = await Request.create_request(
            id=generate_random_string(),
            user_id=message.from_user.id,
            type=Request.RequestType.calculator,
            calculator_data=calculator_data,
            calculator_photo=calculator_photo,
        )

        # send request to manager
        await send_new_request(request=request, bot=dialog_manager.event.bot)

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
            id=generate_random_string(),
            user_id=callback.from_user.id,
            type=Request.RequestType.manager_support,
            support_data=support_data,
        )

        # send request to manager
        await send_new_request(request=request, bot=dialog_manager.event.bot)

        await callback.message.answer(text=_('REQUEST_INFO', request_id=request.id))
        await dialog_manager.start(MainMenuStateGroup.menu)
