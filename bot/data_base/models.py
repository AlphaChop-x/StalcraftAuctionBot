from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import Update, Select

engine = create_async_engine(url="sqlite+aiosqlite:///C:/Users/Was_a/PycharmProjects/StalcraftNewBot/db.sqlite3")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Marked(Base):
    __tablename__ = "marked_items_table"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    marked_items: Mapped[str] = mapped_column(String(120))


class Message(Base):
    __tablename__ = "chat_messages"

    chat_id: Mapped[int] = mapped_column()
    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column()


class Artefact(Base):
    __tablename__ = "artefacts"

    artefact_name: Mapped[str] = mapped_column(unique=True, primary_key=True)
    artefact_id: Mapped[str] = mapped_column(unique=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
