import logging
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.calculator import CalculatorStateGroup
from core.states.main_menu import MainMenuStateGroup
from core.database.models import User, Post
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
