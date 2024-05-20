import logging
import asyncio
from aiogram import types, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.database.models import Request, Currency
from core.states.manager import ManagerStateGroup
from core.utils.texts import set_admin_commands, _
from settings import settings


logger = logging.getLogger(__name__)
router = Router(name='Basic commands router')


# ez to get id while developing
@router.channel_post(Command(commands=['init']))
@router.message(Command(commands=['init']))
async def init_for_id(message: types.Message):
    await message.delete()
    msg = await message.answer(text=f'<code>{message.chat.id}</code>')
    await asyncio.sleep(2)
    await msg.delete()


@router.callback_query(lambda c: 'add_comment_' in c.data)
async def manager_comment_handler(callback: types.CallbackQuery, state: FSMContext):
    request_id = callback.data.split('_')[-1]

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text=_('HANDLE_REQUEST', request_id=request_id))

    await state.update_data(request_id=request_id)
    await state.set_state(ManagerStateGroup.input_comment)


@router.message(ManagerStateGroup.input_comment)
async def input_comment_handler(message: types.Message, bot: Bot, state: FSMContext):
    state_data = await state.get_data()

    request = await Request.get(id=state_data['request_id'])
    request.manager_answer = message.text
    await request.save()

    # send msg to user and manager
    await bot.send_message(chat_id=request.user_id, text=_('REQUEST_ANSWER', request_id=request.id))
    await message.copy_to(chat_id=request.user_id)

    await message.answer(text=_('HANDLE_REQUEST_DONE', request_id=request.id))
    await state.clear()


@router.channel_post(lambda m: m.text and 'Курс сегодня ' in m.text)
async def handle_currency(message: types.Message):
    if str(message.chat.id) != str(settings.required_channel_id):
        return
    currency = message.text
    await Currency.update_or_create(defaults={'currency': currency})
