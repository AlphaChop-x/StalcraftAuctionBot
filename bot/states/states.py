from aiogram.fsm.state import StatesGroup, State


class Artefact(StatesGroup):
    artefact_name = State()
    artefact_rarity = State()
    lots_count = State()
    return_lots = State()
