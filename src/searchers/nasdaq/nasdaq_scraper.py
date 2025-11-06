import asyncio
from enum import StrEnum
from typing import Literal

import curl_cffi as cff

from src.searchers.utils import BaseScraper


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


class NasdaqScraper(BaseScraper):
    def __init__(self, session: cff.AsyncSession, ticker: str):
        self.ticker = ticker
        self.session = session

    def collect_tasks(
            self,
            rows_per_page: Literal[10, 25, 50, 100] = 100,
            limit_pages: int = 5,
    ) -> list[asyncio.Task]:
        tasks = [
            asyncio.create_task(self.get_news(url, i))
            for i, url in enumerate(URLS.iter_pages(
                self.ticker, rows_per_page, limit_pages
            ))
        ]
        return tasks

    async def get_news(self, url: str, identifier: int = 0) -> str:
        response = await self.session.get(url=url)
        if response.status_code != 200:
            raise ValueError(
                f"NasdaqScraper response code: {response.status}, "
                f"reason: {response.reason} "
                f"for ticker: {self.ticker}"
            )

        filename = f"{self.ticker}_{identifier}.html"
        await self._save_file(filename, response.content, is_binary=True)
        return filename
