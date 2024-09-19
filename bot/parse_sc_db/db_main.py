import json
import os
from sqlalchemy import select
from bot.data_base.models import Artefact
from bot.data_base.models import async_session

import asyncio


def parse_artefact(file: os.path):
    with open(f"{file}", "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
        art_id = data["id"]
        art_name = data["name"]["lines"]["ru"]
    print(art_id, art_name)
    return [str(art_id), str(art_name)]


async def is_in_data_base(artefact_id: str, artefact_name: str):
    async with async_session() as session:
        artefact_name = artefact_name.lower()
        is_in_db = await session.scalar(
            select(Artefact).where(Artefact.artefact_name == artefact_name))

        if not is_in_db:
            session.add(Artefact(artefact_id=artefact_id, artefact_name=artefact_name))
            await session.commit()


class ListPath:
    def __init__(self) -> None:
        self.ls = []

    def walk_file(self, path) -> list:
        for i_file in os.listdir(path):
            if os.path.isdir(f'{path}/{i_file}'):
                print(f'Переходим в папку: {i_file}')
                self.walk_file(f'{path}/{i_file}')
            if i_file.endswith(".json"):
                art = parse_artefact(f'{path}/{i_file}')
                asyncio.run(is_in_data_base(artefact_name=str(art[1]), artefact_id=str(art[0])))

