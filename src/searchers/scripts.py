import aiohttp as aio
import pandas as pd

from src.searchers.edgar import EdgarParser, EdgarScraper
from src.searchers.engines_config import EdgarConfig


async def run_edgar(cik: str, session: aio.ClientSession, config: EdgarConfig) -> pd.DataFrame:
    scraper = EdgarScraper(cik, session, config)
    filename = await scraper.scrap_xbrl()
    parser = EdgarParser(filename)
    df = parser.parse()
    return df
