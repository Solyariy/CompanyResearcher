import aiohttp as aio
import pandas as pd

from src.searchers.edgar import EdgarParser, EdgarScraper
from src.searchers.engines_config import EdgarConfig
from src.searchers.macrotrends import MTScraper, MTParser


async def run_edgar(ticker: str, session: aio.ClientSession, config: EdgarConfig) -> pd.DataFrame:
    scraper = EdgarScraper(ticker, session, config)
    filename = await scraper.scrap_xbrl()
    parser = EdgarParser(filename)
    df = parser.parse()
    return df


async def run_mt_history(ticker: str, session: aio.ClientSession) -> pd.DataFrame:
    scraper = MTScraper(session, ticker)
    filename = await scraper.save_full_history_csv()
    parser = MTParser(filename=filename)
    df = parser.parse()
    return df
