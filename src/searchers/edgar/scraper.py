import aiohttp as aio
from fastapi import HTTPException
from typing import Any
import os
from dotenv import load_dotenv
load_dotenv()


class EdgarScraper:
    def __init__(self, cik: str, session: aio.ClientSession):
        self.cik = cik
        self.session = session
        self._user_agent_header = os.environ.get("EDGAR_HEADER")

    async def scrap_xbrl(self) -> dict[str, Any]:
        headers = {
            "User-Agent": self._user_agent_header
        }
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json"
        async with self.session.get(url=url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(response.status, response.content)
            data: dict[str, Any] = await response.json()
        return data["facts"]["us-gaap"]
