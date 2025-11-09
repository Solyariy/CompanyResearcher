from typing import Any

import aiohttp as aio
from fastapi import HTTPException

from src.searchers.engines_config import EdgarConfig
from src.searchers.utils import BaseScraper, get_cik


class EdgarScraper(BaseScraper):
    def __init__(self, ticker: str, session: aio.ClientSession, config: EdgarConfig):
        self.ticker = ticker
        self.cik = get_cik(ticker)
        self.session = session
        self.__config = config

    async def scrap_xbrl(self) -> str:
        headers = {
            "User-Agent": self.__config.header
        }
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json"
        async with self.session.get(url=url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(response.status, response.content)
            data: dict[str, Any] = await response.json()
        filename = f"{self.ticker}_edgar_report.json"
        await self._save_file(filename, data, as_json=True)
        return filename
