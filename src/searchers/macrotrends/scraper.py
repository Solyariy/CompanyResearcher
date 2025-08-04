import json
import os
from enum import StrEnum
from pathlib import Path
from typing import Any

import aiofiles
import aiohttp as aio

from src.searchers.emulator import ChromeEmulator

FILEPATH = os.path.join(Path(__file__).resolve().parents[1], "test_files")


class URLS(StrEnum):
    DOMAIN = "https://www.macrotrends.net"
    STOCKS = DOMAIN + "/stocks/stock-screener"
    HISTORY = DOMAIN + "/assets/php/stock_data_download.php?t={ticker}"


class MTScraper:
    def __init__(self, session: aio.ClientSession):
        self.session = session

    async def save_full_history_csv(self, tickers: list[str]):
        for ticker in tickers:
            url = URLS.HISTORY.format(ticker=ticker)
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise ValueError()
                data = await response.text()
                data = data[data.find("date,open"):].rstrip()
                filepath = os.path.join(FILEPATH, f"{ticker}_full_history.csv")
                async with aiofiles.open(filepath, "w") as f:
                    await f.write(data)

    async def get_stocks_data(self) -> list[dict[str, Any]]:
        async with self.session.get(URLS.STOCKS) as response:
            if response.status != 200:
                raise ValueError(response)
            data = await response.text()
            data = data[data.find("originalData = [") + len("originalData = [") - 1:]
            data = data[:data.find("var filterArray")].strip().removesuffix(";")
            data = json.loads(data)
            return data
