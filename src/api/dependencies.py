import aiohttp
from fastapi import Request

from src.searchers.engines_config import GoogleConfig, GoogleAlertsConfig


def get_session(request: Request) -> aiohttp.ClientSession:
    return request.app.state.aio_session

def get_google_config(request: Request) -> GoogleConfig:
    return request.app.state.google_config

def get_google_alerts_config(request: Request) -> GoogleAlertsConfig:
    return request.app.state.google_alerts_config