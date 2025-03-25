from aiogram.fsm.state import StatesGroup, State

class SourcesFSM(StatesGroup):
    WAITING_FOR_URL = State()