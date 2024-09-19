from bot.data_base.models import async_session
from bot.data_base.models import Artefact
from sqlalchemy import select, update

import asyncio

import json
import requests


class StalcraftApi:
    rarity_cases = {0: "обычный",
                    1: "необычный",
                    2: "особый",
                    3: "редкий",
                    4: "исключительный",
                    5: "легендарный"}

    client = {"Client-Id": "614",
              "Client-Secret": "hNygXAGgdZBpRMrPPpvefbUXYUkrnxFHRWSRYiAw"}

    BASE_URL = "https://eapi.stalcraft.net/ru"

    params = {"additional": True,
              "limit": 200,
              "sort": "buyout_price"}

    def __init__(self, artefact, rarity, lots_count):
        self.art_name = artefact
        self.rarity = rarity
        self.count_of_lots = lots_count

    @staticmethod
    async def get_artefact_id_by_name(artefact_name: str) -> str:
        async with async_session() as session:
            lower_name = artefact_name.lower()

            artefact_id = await session.scalar(
                select(Artefact.artefact_id).where(Artefact.artefact_name == lower_name))
            if artefact_id:
                return artefact_id
            raise ValueError("Артефакт не обнаружен")

    @classmethod
    def get_response_by_artefact_id(cls, artefact_id):
        response = requests.get(f"{cls.BASE_URL}/auction/{artefact_id}/lots", headers=cls.client, params=cls.params)
        response_lots = response.json()["lots"]
        lots_count = response.json()["total"]
        return response_lots, lots_count

    @classmethod
    def return_necessary_values(cls, json_lot) -> {str}:
        values = list()
        values.append(json_lot["buyoutPrice"])
        if "qlt" in json_lot["additional"]:
            values.append(json_lot["additional"]["qlt"])
        else:
            values.append(0)
        if "ptn" in json_lot["additional"]:
            values.append(json_lot["additional"]["ptn"])
        else:
            values.append(0)
        return values

    @classmethod
    def get_values_by_all_lots(cls, auction_lots) -> list[list]:
        all_lots_values = list(list())
        for k_lot in auction_lots:
            all_lots_values.append(cls.return_necessary_values(k_lot))
        return all_lots_values

    async def return_artefact_lots(self) -> None:
        art_id = await self.get_artefact_id_by_name(self.art_name)
        art_lots, active_lots_count = self.get_response_by_artefact_id(artefact_id=art_id)
        if active_lots_count > 200:
            self.params.update({"offset": 200})
            another_lots = self.get_response_by_artefact_id()
            art_lots += another_lots

        target_lots_count = 0
        answer_data = list(list())

        for i_lot in art_lots:
            data = self.return_necessary_values(i_lot)
            if data[1] == self.rarity and data[0] != 0:
                answer_data.append(data)
                target_lots_count += 1
        if answer_data:
            return answer_data, target_lots_count
        else:
            return "Артефакты не найдены"


async def to_beautiful_string(arr: list[list], lots_count) -> str:
    beautiful_string = ""
    if arr[0] is not None:
        beautiful_string += f"Количество найденных лотов: {lots_count}\n\n"
        for i_artefact in arr:
            string = (f"Цена лота: {i_artefact[0]}"
                      f"\nРедкость Артефакта: {StalcraftApi.rarity_cases[i_artefact[1]]}"
                      f"\nЗаточка Артефакта: +{i_artefact[2]}\n")
            beautiful_string += string
        return beautiful_string
    else:
        return "Лоты не обнаружены"


@staticmethod
async def is_artefact_exist(artefact_name: str) -> bool:
    async with async_session() as session:
        lower_name = artefact_name.lower()

        exist = await session.scalar(
            select(Artefact.artefact_id).where(Artefact.artefact_name == lower_name))
        if exist:
            return True
        else:
            return False
