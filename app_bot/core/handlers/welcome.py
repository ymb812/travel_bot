import logging
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram_dialog import DialogManager, StartMode
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import set_user_commands, _
from core.database.models import User, Post
from settings import settings


logger = logging.getLogger(__name__)
router = Router(name='Start router')


@router.message(Command(commands=['start']), StateFilter(None))
async def start_handler(
        message: types.Message,
        bot: Bot,
        state: FSMContext,
        dialog_manager: DialogManager,
        command: CommandObject,
):
    await state.clear()
    try:
        await dialog_manager.reset_stack()
    except:
        pass

    # add basic info to db
    await User.update_data(
        user_id=message.from_user.id,
        username=message.from_user.username,
    )

    await set_user_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
    welcome_post = await Post.get(id=settings.welcome_post_id)
    await message.answer_video(
        caption=welcome_post.text,
        video=welcome_post.video_file_id,
    )

    # send main menu
    await dialog_manager.start(state=MainMenuStateGroup.menu, mode=StartMode.RESET_STACK)
