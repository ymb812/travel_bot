from aiogram.fsm.state import State, StatesGroup


class MainMenuStateGroup(StatesGroup):
    menu = State()

    pick_info = State()
    info = State()

    pick_requirements = State()
    requirements = State()

    pick_faq = State()
    faq = State()

    cases_reviews_currency = State()
