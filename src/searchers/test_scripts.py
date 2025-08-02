import aiohttp as aio
from src.searchers.scripts import run_edgar


async def test_edgar(cik: str = "0000320193", csv_name: str = "edgar_test"):
    async with aio.ClientSession(
            connector=aio.TCPConnector(ssl=False)
    ) as session:
        df = await run_edgar("0000320193", session)
    df.to_csv(f"{csv_name}_{cik}")
