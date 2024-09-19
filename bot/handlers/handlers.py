from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import bot.keyboards.keyboards as kb
import bot.data_base.requests as rq

router = Router(name='sigma')


@router.message(CommandStart())
async def register_new_user(message: Message):

    await message.delete()
    await rq.set_user(message.from_user.id)

    new_message = await message.answer(
        "Добро пожаловать в бота ArtefactFinder\n"
        "Для начала работы с ботом, пожалуйста, выберите пункт меню",
        reply_markup=kb.commands_kb)

    try:
        message_to_delete = await rq.get_message_id(message.chat.id)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message_to_delete)
    except ValueError:
        pass

    await rq.set_message_id(chat_id=message.chat.id, message_id=new_message.message_id)
