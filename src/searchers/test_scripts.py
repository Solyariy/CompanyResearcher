import asyncio
import functools as ft
import os
import sys
from pathlib import Path

import aiohttp as aio
import curl_cffi as cff
import pandas as pd

from src.searchers.engines_config import EdgarConfig
from src.searchers.macrotrends.scraper import MTScraper
from src.searchers.nasdaq.scraper import NasdaqScraper
from src.searchers.scripts import run_edgar

FILEPATH = os.path.join(Path(__file__).resolve().parent, "test_files")


async def test_edgar(cik: str = "0000320193", csv_name: str = "edgar_test"):
    file_dir = os.path.dirname(__file__)
    path = os.path.join(file_dir, "test_files", csv_name)
    config = EdgarConfig()
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        df = await run_edgar(cik, session, config)
    df.to_csv(f"{path}_{cik}.csv")


async def test_macrotrends_stocks(csv_name_all: str = "macro_test_all_stocks"):
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        scraper = MTScraper(session, "")
        stock_data = await scraper.get_all_stocks_analysis()
        pd.DataFrame(stock_data).to_csv(os.path.join(FILEPATH, csv_name_all + ".csv"), index=False)


async def test_macrotrends_history(ticker: str = "A"):
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        scraper = MTScraper(session, ticker)
        await scraper.save_full_history_csv()

# TODO - add nasdaq test to bash script
async def test_nasdaq_collect_news(rows_per_page: int = 10, limit_pages: int = 1):
    async with cff.AsyncSession() as session:
        scraper = NasdaqScraper(session, "AAPL")
        tasks = scraper.collect_tasks(rows_per_page, limit_pages)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 2:
        print("Usage: python3 -m src.searchers.test_scripts <test_func_name>")
        sys.exit(1)
    func_name = arguments[1]
    func_body = globals().get(func_name)
    if func_name == "test_macrotrends_history":
        ticker = arguments[2] or "A"
        func_body = ft.partial(func_body, ticker=ticker)
    if func_body and callable(func_body):
        asyncio.run(func_body())
    else:
        print(f"No such test function: {func_name}")
