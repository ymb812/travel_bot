from aiogram.fsm.state import State, StatesGroup


class ManagerStateGroup(StatesGroup):
    input_fio = State()
    sell_and_delivery = State()
    from_where = State()
    send_data = State()
