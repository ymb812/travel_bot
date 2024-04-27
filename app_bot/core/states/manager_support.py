from aiogram.fsm.state import State, StatesGroup


class ManagerSupportStateGroup(StatesGroup):
    input_fio = State()
    sell_and_delivery = State()
    did_work = State()
    from_where = State()
    send_data = State()
