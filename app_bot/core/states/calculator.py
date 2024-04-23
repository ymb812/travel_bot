from aiogram.fsm.state import State, StatesGroup


class CalculatorStateGroup(StatesGroup):
    menu = State()
    input_calculator_data = State()
    manager_help = State()
