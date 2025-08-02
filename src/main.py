from contextlib import asynccontextmanager
from time import perf_counter

import aiohttp
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware

from src.api.main_router import router as main_router
from src.searchers.engines_config import GoogleAlertsConfig, GoogleConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.google_config = GoogleConfig()
    app.state.google_alerts_config = GoogleAlertsConfig()
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        app.state.aio_session = session
        yield


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)


@app.middleware("http")
async def test_middleware(request: Request, call_next):
    start = perf_counter()
    response: Response = await call_next(request)
    spent_time = perf_counter() - start
    response.headers["X-Process-Time"] = str(spent_time)
    return response
