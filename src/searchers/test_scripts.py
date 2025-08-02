import os

import aiohttp as aio

from src.searchers.engines_config import EdgarConfig
from src.searchers.scripts import run_edgar


async def test_edgar(cik: str = "0000320193", csv_name: str = "edgar_test"):
    file_dir = os.path.dirname(__file__)
    path = os.path.join(file_dir, "test_files", csv_name)
    config = EdgarConfig()
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        df = await run_edgar(cik, session, config)
    df.to_csv(f"{path}_{cik}.csv")
