from aiogram.fsm.state import State, StatesGroup


class ManagerStateGroup(StatesGroup):
    input_comment = State()
