from typing import Any

import aiohttp as aio
from fastapi import HTTPException

from src.searchers.engines_config import EdgarConfig


class EdgarScraper:
    def __init__(self, cik: str, session: aio.ClientSession, config: EdgarConfig):
        self.cik = cik
        self.session = session
        self.__config = config

    async def scrap_xbrl(self) -> dict[str, Any]:
        headers = {
            "User-Agent": self.__config.header
        }
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json"
        async with self.session.get(url=url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(response.status, response.content)
            data: dict[str, Any] = await response.json()
        return data["facts"]["us-gaap"]
