from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    steps = State()
class AdminStates(StatesGroup):
    ...

class ManageStates(StatesGroup):
    ...
