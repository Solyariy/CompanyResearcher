import pandas as pd
import aiohttp as aio
from src.searchers.edgar import EdgarScraper, EdgarParser


async def run_edgar(cik: str, session: aio.ClientSession) -> pd.DataFrame:
    scraper = EdgarScraper(cik, session)
    data = await scraper.scrap_xbrl()
    parser = EdgarParser(data)
    df = parser.parse()
    return df
