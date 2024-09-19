import logging

from aiogram import Bot, Dispatcher
from bot.handlers.handlers import router as sigma
from bot.handlers.callbacks import router as alpha
from bot.handlers.states_hand import router as beta

from bot.data_base.models import async_main
from bot.parse_sc_db import db_main

dp = Dispatcher()


async def start_bot(token):
    await async_main()
    bot = Bot(token=token)
    dp.include_router(sigma)
    dp.include_router(alpha)
    dp.include_router(beta)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)
