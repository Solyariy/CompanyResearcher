import curl_cffi as cff
import os
from enum import StrEnum
from pathlib import Path
from typing import Literal
import asyncio
import aiofiles

FILEPATH = os.path.join(Path(__file__).resolve().parents[1], "test_files")


class URLS(StrEnum):
    DOMAIN = "https://www.nasdaq.com"
    NEWS_PATH = DOMAIN + "/market-activity/stocks/{ticker}/news-headlines"

    @classmethod
    def validate_params(cls, rows_per_page, limit_pages):
        if rows_per_page not in (10, 25, 50, 100):
            raise ValueError(
                "NasdaqScraper accepts only "
                "[10, 25, 50, 100] numbers for rows per page "
                f"but {rows_per_page=}"
            )
        if limit_pages < 1:
            raise ValueError(
                "NasdaqScraper accepts only "
                f"limit_pages >= 1, but {limit_pages=}"
            )

    @classmethod
    def iter_pages(
            cls,
            ticker: str,
            rows_per_page: Literal[10, 25, 50, 100] = 100,
            limit_pages: int = 5,
    ):
        cls.validate_params(rows_per_page, limit_pages)
        url = (cls.NEWS_PATH.format(ticker=ticker)
               + "?page={page_num}&rows_per_page={rows_per_page}")
        total_rows = rows_per_page
        page_num = 1
        while total_rows <= 500 and page_num <= limit_pages:
            yield url.format(page_num=page_num, rows_per_page=rows_per_page)
            page_num += 1
            total_rows += rows_per_page


class NasdaqScraper:
    def __init__(self, session: cff.AsyncSession):
        self.session = session

    @staticmethod
    async def _save_to_csv(filepath, data):
        async with aiofiles.open(filepath + ".html", "wb") as f:
            await f.write(data)

    def collect_tasks(
            self,
            ticker: str,
            rows_per_page: Literal[10, 25, 50, 100] = 100,
            limit_pages: int = 5,
    ) -> list[asyncio.Task]:
        tasks = [
            asyncio.create_task(self.get_news(url, ticker, i))
            for i, url in enumerate(URLS.iter_pages(ticker, rows_per_page, limit_pages))
        ]
        print(len(tasks))
        return tasks

    async def get_news(self, url: str, ticker: str, i: int) -> bytes:
        response = await self.session.get(url=url)
        if response.status_code != 200:
            raise ValueError(
                f"NasdaqScraper response code: {response.status}, "
                f"reason: {response.reason} "
                f"for ticker: {ticker}"
            )
        await self._save_to_csv(f"{ticker}_{i}", response.content)


async def main():
    async with cff.AsyncSession() as session:
        scraper = NasdaqScraper(session)
        tasks = scraper.collect_tasks("AAPL", 10, 3)
        await asyncio.gather(*tasks, return_exceptions=True)

async def sth():
    async with cff.AsyncSession() as session:
        scraper = NasdaqScraper(session)
        url = next(URLS.iter_pages("AAPL", 10, 1))
        await scraper.get_news(url, "AAPL")



if __name__ == '__main__':
    asyncio.run(main())
