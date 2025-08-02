import os

import aiohttp as aio
import asyncio
import sys
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


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 2:
        print("Usage: python3 -m src.searchers.test_scripts <test_func_name>")
        sys.exit(1)

    func_name = arguments[1]
    func_body = globals().get(func_name)
    if func_body and callable(func_body):
        asyncio.run(func_body())
    else:
        print(f"No such test function: {func_name}")
