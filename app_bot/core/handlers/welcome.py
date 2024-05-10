import logging
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram_dialog import DialogManager, StartMode
from core.states.main_menu import MainMenuStateGroup
from core.states.manager import ManagerStateGroup
from core.utils.texts import set_user_commands, set_admin_commands, _
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
    user = await User.update_data(
        user_id=message.from_user.id,
        username=message.from_user.username,
    )

    if user.status == 'admin':
        await set_admin_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
    else:
        await set_user_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))

    # send manager_menu or main_menu
    if user.status == User.StatusType.manager.value:
        await dialog_manager.start(state=ManagerStateGroup.manager_menu, mode=StartMode.RESET_STACK)

    else:
        welcome_post = await Post.get(id=settings.welcome_post_id)
        await message.answer_video(
            caption=welcome_post.text,
            video=welcome_post.video_file_id,
        )

        await dialog_manager.start(state=MainMenuStateGroup.menu, mode=StartMode.RESET_STACK)
