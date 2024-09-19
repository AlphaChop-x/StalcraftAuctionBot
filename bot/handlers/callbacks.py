from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import bot.keyboards.keyboards as kb
import bot.states.states as st
import bot.data_base.requests

router = Router(name="alpha")


@router.callback_query(F.data == "marked_items")
async def marked(call: CallbackQuery):
    await call.message.edit_text("Функция в разработке!", reply_markup=kb.go_back_kb)


@router.callback_query(F.data == "items_list")
async def items_list(call: CallbackQuery):
    await call.message.edit_text("Функция в разработке!", reply_markup=kb.go_back_kb)


@router.callback_query(F.data == "developer")
async def developer_info(call: CallbackQuery):
    await call.message.edit_text("Вам это знать не положено!", reply_markup=kb.go_back_kb)


@router.callback_query(F.data == "arts_list")
async def artefacts(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Напишите название артефакта\nВажно! Название пишите ровно так, как оно написано в игре\n"
        "Не обязательно писать в том-же регистре",
        reply_markup=kb.go_back_kb)
    await state.set_state(st.Artefact.artefact_name)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text("Добро пожаловать в бота ArtefactFinder\n"
                                 "Для начала работы с ботом, пожалуйста, выберите пункт меню",
                                 reply_markup=kb.commands_kb)
