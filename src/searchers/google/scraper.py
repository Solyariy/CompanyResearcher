import asyncio
from typing import Annotated, Any

import aiohttp
from fastapi import HTTPException
from pydantic import StringConstraints, validate_call

from src.searchers.engines_config import GoogleConfig


class GoogleEngine:
    URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]

    def __init__(self, session: aiohttp.ClientSession, config: GoogleConfig):
        self.session = session
        self.config = config

    async def request(self, query: str, full_link: bool = False):
        req = f"{self.config.build_url()}{query}"
        response = await self.__send_request(req)
        return await asyncio.to_thread(self._get_urls, response, full_link)

    @validate_call
    async def __send_request(self, request: URL_PATTERN):
        async with self.session.get(request) as response:
            if response.status != 200:
                raise HTTPException(response.status, response)
            return await response.json()

    @staticmethod
    def _get_urls(response: dict[str, Any], full_link: bool) -> set[str]:
        key = "link" if full_link else "displayLink"
        return set(
            item.get(key)
            for item in response.get("items")
        )
