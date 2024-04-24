import logging
import uuid
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.calculator import CalculatorStateGroup
from core.states.main_menu import MainMenuStateGroup
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

        request = await Request.create(
            id=uuid.uuid4(),
            user_id=message.from_user.id,
            type=Request.RequestType.calculator,
            calculator_data=message.text,
            calculator_photo=calculator_photo,
        )

        await message.answer(text=_('CALCULATOR_REQUEST_INFO', request_id=request.id))
        await dialog_manager.switch_to(MainMenuStateGroup.menu)


    @classmethod
    async def main_menu_content(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        pass


    @staticmethod
    async def entered_fio(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value: str,
    ):
        pass
