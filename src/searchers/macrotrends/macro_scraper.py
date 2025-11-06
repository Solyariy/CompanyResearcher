from enum import StrEnum

import aiohttp as aio
import pandas as pd
from src.searchers.utils import BaseScraper


class URLS(StrEnum):
    DOMAIN = "https://www.macrotrends.net"
    STOCKS = DOMAIN + "/stocks/stock-screener"
    HISTORY = DOMAIN + "/assets/php/stock_data_download.php?t={ticker}"


class MTScraper(BaseScraper):
    def __init__(self, session: aio.ClientSession, ticker: str = None):
        self.ticker = ticker
        self.session = session

    async def save_full_history_csv(self) -> str:
        if not self.ticker:
            raise ValueError("No ticker provided")
        url = URLS.HISTORY.format(ticker=self.ticker)
        async with self.session.get(url) as response:
            if response.status != 200:
                raise ValueError(
                    f"MTScraper response code: {response.status}, "
                    f"for ticker: {self.ticker}"
                )
            data = await response.text()
        data = data[data.find("date,open"):].rstrip()
        filename = f"{self.ticker}_full_stock_price_history.csv"
        await self._save_file(filename, data)
        return filename

    async def get_all_stocks_analysis(self) -> str:
        async with self.session.get(URLS.STOCKS) as response:
            if response.status != 200:
                raise ValueError(response)
            data = await response.text()
        data = data[data.find("originalData = [") + len("originalData = [") - 1:]
        data = data[:data.find("var filterArray")].strip().removesuffix(";")
        filename = "macro_all_stocks_analysis.json"
        await self._save_file(filename, data)
        return filename
