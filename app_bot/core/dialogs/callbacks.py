import logging
import string
import random
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.main_menu import MainMenuStateGroup
from core.states.manager_support import ManagerSupportStateGroup
from core.states.manager import ManagerStateGroup
from core.database.models import User, Request, RequestLog, ManagerCard
from core.keyboards.inline import add_comment_kb
from core.user_manager.user_manager import add_manager_to_user
from core.utils.texts import _

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


async def switch_page(dialog_manager: DialogManager, scroll_id: str, message: Message):
    # switch page
    scroll: ManagedScroll = dialog_manager.find(scroll_id)
    current_page = await scroll.get_page()

    if current_page == dialog_manager.dialog_data['pages'] - 1:
        next_page = 0
    else:
        next_page = current_page + 1
    await scroll.set_page(next_page)


# end of calculator
async def create_new_request(dialog_manager: DialogManager, user_id: int, bot: Bot):
    calculator_data = dialog_manager.dialog_data['input_weight'] + dialog_manager.dialog_data['input_length'] +\
                      dialog_manager.dialog_data['input_width'] + dialog_manager.dialog_data['input_height'] +\
                      dialog_manager.dialog_data['input_density']
    request = await Request.create_request(
        id=generate_random_string(),
        user_id=user_id,
        type=Request.RequestType.calculator,
        calculator_data=calculator_data,
        calculator_photo=dialog_manager.dialog_data.get('calculator_photo'),
    )

    # send request to manager
    await send_new_request(request=request, bot=dialog_manager.event.bot)

    await bot.send_message(chat_id=user_id, text=_('REQUEST_INFO', request_id=request.id))
    await dialog_manager.switch_to(MainMenuStateGroup.menu)


async def send_new_request(request: Request, bot: Bot):
    user: User = await request.user

    # pick manager for user
    manager_to_send = await add_manager_to_user(user_id=user.user_id, request_id=request.id)
    if not manager_to_send:
        return

    # send request (calculator/support)
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

    # add log with request and add manager to request
    await RequestLog.create_log(manager_id=manager_to_send.user_id, user_id=user.user_id, request_id=request.id)

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

    @classmethod
    async def selected_case(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        dialog_manager.dialog_data['case_id'] = item_id
        await dialog_manager.switch_to(MainMenuStateGroup.case)


    @staticmethod
    async def entered_calculator_text_data(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value: str
    ):
        if widget.widget_id == 'input_weight':
            dialog_manager.dialog_data['input_weight'] = f'Вес: {value}\n'
            await dialog_manager.switch_to(MainMenuStateGroup.input_length)
            return

        elif widget.widget_id == 'input_length':
            dialog_manager.dialog_data['input_length'] = f'Длина: {value}\n'
            await dialog_manager.switch_to(MainMenuStateGroup.input_width)
            return

        elif widget.widget_id == 'input_width':
            dialog_manager.dialog_data['input_width'] = f'Ширина: {value}\n'
            await dialog_manager.switch_to(MainMenuStateGroup.input_height)
            return

        elif widget.widget_id == 'input_height':
            dialog_manager.dialog_data['input_height'] = f'Высота: {value}\n'
            await dialog_manager.switch_to(MainMenuStateGroup.input_density)
            return

        elif widget.widget_id == 'input_density':
            dialog_manager.dialog_data['input_density'] = f'Плотность: {value}\n'
            await dialog_manager.switch_to(MainMenuStateGroup.input_photo)
            return


    # create new calculator request
    @staticmethod
    async def entered_calculator_photo(
            message: Message,
            widget: MessageInput,
            dialog_manager: DialogManager,
    ):
        calculator_data = message.text
        calculator_photo = None
        if message.photo:
            calculator_data = message.caption
            calculator_photo = message.photo[-1].file_id

        dialog_manager.dialog_data['calculator_photo'] = calculator_photo
        await create_new_request(
            dialog_manager=dialog_manager,
            user_id=message.from_user.id,
            bot=dialog_manager.event.bot
        )  # end of calculator


    # skip photo
    @classmethod
    async def create_new_request(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        dialog_manager.dialog_data['calculator_photo'] = None
        await create_new_request(
            dialog_manager=dialog_manager,
            user_id=callback.from_user.id,
            bot=dialog_manager.event.bot
        )  # end of calculator


    # add manager_id and send 2 msg
    @classmethod
    async def start_manager_support(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # add manager and log for future working
        manager_to_send = await add_manager_to_user(user_id=callback.from_user.id, without_request=True)

        await dialog_manager.start(state=ManagerSupportStateGroup.input_fio)


    # add manager_id and start dialog
    @classmethod
    async def send_msg_to_manager(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        user = await User.get_or_none(user_id=callback.from_user.id)
        if not user:
            await callback.message.answer(text='Пропишите /start и попробуйте снова')
            return

        # add manager and log for future working
        try:
            manager_to_send = await add_manager_to_user(user_id=callback.from_user.id, without_request=True)
        except Exception as e:
            logger.error(f'Error to pin manager to user_id={callback.from_user.id}', exc_info=e)
            return

        # send info msg to user and notification to manager
        if manager_to_send:
            await callback.message.answer(text='Наш менеджер свяжется с вами в ближайшее время')
            await dialog_manager.event.bot.send_message(
                chat_id=manager_to_send.user_id,
                text=f'Обратился клиент {get_username_or_link(user=user)} - не знает данных'
            )
        else:
            await callback.message.answer(text='Активных менеджеров нет - обратитесь в поддержку')

        await dialog_manager.switch_to(state=MainMenuStateGroup.menu)


    # open managers_cards
    @classmethod
    async def open_managers_cards(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # check if there are any users here
        managers_cards = await ManagerCard.all()
        if not managers_cards:
            await callback.message.answer(text='Информации о менеджерах пока нет...')
            return

        await dialog_manager.switch_to(MainMenuStateGroup.managers_cards)


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
        else:
            return

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


class ManagerCallbackHandler:
    @classmethod
    async def selected_status(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        # check if there are any users here
        users = await User.filter(
            manager_id=dialog_manager.event.from_user.id,
            status=item_id,
        )

        if not users:
            await callback.message.answer(text='Пользователей с таким статусом нет')
            return

        dialog_manager.dialog_data['filter_by_status'] = item_id
        await dialog_manager.switch_to(ManagerStateGroup.users_list)


    @classmethod
    async def change_user_status(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        # update status
        status = dialog_manager.dialog_data['statuses_dict'][item_id]
        await User.filter(user_id=dialog_manager.dialog_data['current_user_user_id']).update(
            status=status,
        )

        # switch page
        await switch_page(dialog_manager=dialog_manager, scroll_id='user_scroll', message=callback.message)

        # last page - bypass IndexError
        if dialog_manager.dialog_data['pages'] == 1:
            await dialog_manager.switch_to(ManagerStateGroup.manager_menu)
