from bot.data_base.models import async_session
from bot.data_base.models import User, Marked, Message
from sqlalchemy import select, update, delete


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_message_id(chat_id: int) -> int:
    async with async_session() as session:
        message_id = await session.scalar(
            select(Message.message_id).where(Message.chat_id == chat_id))

        if not message_id:
            raise ValueError("Отсутствует ID сообщения")

        return message_id


async def set_message_id(chat_id: int, message_id: int) -> None:
    async with async_session() as session:
        exists = await session.scalar(select(Message).where(Message.chat_id == chat_id))
        if exists:
            await session.delete(exists)
            await session.commit()
        message = Message(chat_id=chat_id, message_id=message_id)
        session.add(message)
        await session.commit()

