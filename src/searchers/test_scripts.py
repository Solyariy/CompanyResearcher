import asyncio
import functools as ft
import os
import sys
from pathlib import Path

import aiohttp as aio
import curl_cffi as cff
import pandas as pd

from src.searchers.engines_config import EdgarConfig
from src.searchers.macrotrends.macro_scraper import MTScraper
from src.searchers.nasdaq.nasdaq_api_scraper import NasdaqApiScraper
from src.searchers.nasdaq.nasdaq_scraper import NasdaqScraper
from src.searchers.scripts import run_edgar, run_mt_history
from src.base_config import FILEPATH


async def test_edgar(ticker: str = "AAPL", csv_name: str = "edgar_test"):
    path = os.path.join(FILEPATH, f"{ticker}_{csv_name}.csv")
    config = EdgarConfig()
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        df = await run_edgar(ticker, session, config)
    df.to_csv(path)


async def test_macrotrends_stocks():
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        scraper = MTScraper(session)
        await scraper.get_all_stocks_analysis()


async def test_macrotrends_history(ticker: str = "AAPL"):
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        df = await run_mt_history(ticker=ticker, session=session)
    df.to_csv(os.path.join(FILEPATH, f"{ticker}_mt_parsed_history.csv"))



# async def test_nasdaq_collect_news(rows_per_page: int = 10, limit_pages: int = 1):
#     async with cff.AsyncSession() as session:
#         scraper = NasdaqScraper(session, "AAPL")
#         tasks = scraper.collect_tasks(rows_per_page, limit_pages)
#         await asyncio.gather(*tasks, return_exceptions=True)


async def test_nasdaq_news(ticker: str = "AAPL", limit: int = 10):
    async with cff.AsyncSession() as session:
        scraper = NasdaqApiScraper(session, ticker)
        filename = await scraper.get_news(limit)



if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 2:
        print("Usage: python3 -m src.searchers.test_scripts <test_func_name>")
        sys.exit(1)
    func_name = arguments[1]
    func_body = globals().get(func_name)
    if func_name == "test_macrotrends_history":
        ticker = arguments[2] or "AAPL"
        func_body = ft.partial(func_body, ticker=ticker)
    if func_name == "test_nasdaq_news":
        ticker = arguments[2] or "AAPL"
        limit = arguments[3] or 10
        func_body = ft.partial(func_body, ticker=ticker, limit=limit)
    if func_body and callable(func_body):
        asyncio.run(func_body())
    else:
        print(f"No such test function: {func_name}")
