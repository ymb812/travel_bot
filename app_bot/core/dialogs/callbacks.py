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
    async def main_menu_content(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        pass


    @classmethod
    async def selected_status(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        pass


    @staticmethod
    async def entered_problem(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value: str,
    ):
        pass
