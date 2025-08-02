import asyncio

import aiohttp
from fastapi import APIRouter, Depends

from src.api.dependencies import (get_google_alerts_config, get_google_config,
                                  get_session)
from src.searchers.engines_config import GoogleAlertsConfig, GoogleConfig
from src.searchers.google import Find, GoogleEngine

router = APIRouter(prefix="/api/v1")


@router.get("/root")
async def root():
    return "Hello"


@router.get("/alerts")
async def alert(
        aio_session: aiohttp.ClientSession = Depends(get_session),
        google_alerts_config: GoogleAlertsConfig = Depends(get_google_alerts_config)
):
    params = await asyncio.to_thread(getattr(google_alerts_config, "get_params"))
    async with aio_session.get(**params) as response:
        return await response.json()



@router.get("/scrap/url")
async def scrap(
        company: str,
        full_link: bool = False,
        aio_session: aiohttp.ClientSession = Depends(get_session),
        google_config: GoogleConfig = Depends(get_google_config)
):
    google_engine = GoogleEngine(aio_session, google_config)
    query = (
        Find(company)
        .include("review", "stock", "stocks")
        .exact_phrase("market analysis")
        .exclude("fruit", "politics", "tiktok")
        .now()
    )
    return {"urls": await google_engine.request(query.build(), full_link)}
