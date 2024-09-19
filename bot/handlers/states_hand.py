from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

import bot.states.states as st
import bot.keyboards.keyboards as kb
import bot.data_base.requests as rq
import bot.stalcraft_api.stalcraft_api as sc

router = Router(name="beta")


@router.message(st.Artefact.artefact_name)
async def chose_artefact(message: Message, state: FSMContext):
    await message.delete()

    if not await sc.is_artefact_exist(message.text):
        new_message = await message.answer("Такого артефакта не существует, Заново введите название!",
                                           reply_markup=kb.go_back_kb)
        try:
            message_to_delete = await rq.get_message_id(message.chat.id)
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message_to_delete)
        except ValueError:
            pass

        await rq.set_message_id(chat_id=message.chat.id, message_id=new_message.message_id)

        await state.set_state(st.Artefact.artefact_name)

    else:
        await state.update_data(artefact_name=message.text)
        await state.set_state(st.Artefact.artefact_rarity)

        new_message = await message.answer("Теперь выберите редкость артефакта!", reply_markup=kb.rarities)

        try:
            message_to_delete = await rq.get_message_id(message.chat.id)
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message_to_delete)
        except ValueError:
            pass

        await rq.set_message_id(chat_id=message.chat.id, message_id=new_message.message_id)


@router.callback_query(F.data.startswith('rarity_'), st.Artefact.artefact_rarity)
async def chose_artefact(call: CallbackQuery, state: FSMContext):
    await call.answer("")
    cur_art_rarity = int(call.data.replace('rarity_', ''))
    await state.update_data(artefact_rarity=cur_art_rarity)
    await call.message.edit_text("Выберите количество лотов на аукционе", reply_markup=kb.find_lots_kb)
    await state.set_state(st.Artefact.lots_count)


@router.callback_query(F.data.startswith('lots_'), st.Artefact.lots_count)
async def choose_lots_count(call: CallbackQuery, state: FSMContext):
    await call.answer("")
    lots_count = int(call.data.replace('lots_', ''))
    await state.update_data(lots_count=lots_count)
    await state.set_state(st.Artefact.return_lots)
    data = await state.get_data()

    artefacts = sc.StalcraftApi(artefact=data['artefact_name'], rarity=data['artefact_rarity'],
                                lots_count=data['lots_count'])
    arts, lots_count = await artefacts.return_artefact_lots()
    await call.message.edit_text(await sc.to_beautiful_string(arts, lots_count), reply_markup=kb.go_back_kb)
    await state.clear()
