import curl_cffi as cff

from src.searchers.utils import BaseScraper


class NasdaqApiScraper(BaseScraper):
    def __init__(self, session: cff.AsyncSession, ticker: str):
        self.ticker = ticker
        self.session = session
        self.url_unformatted = "https://api.nasdaq.com/api/news/topic/articlebysymbol?symbol=AAPL&limit={}"

    def check_response(self, response):
        if response.status_code != 200:
            raise ValueError(
                f"NasdaqApiScraper response code: {response.status_code}, "
                f"reason: {response.reason} "
                f"for ticker: {self.ticker}"
            )

    @staticmethod
    def check_return_data(response):
        resp_data = response.json()
        data = resp_data.get("data")
        if data is None:
            raise ValueError("Retrieved data is None")
        rows = data.get("rows")
        if rows is None:
            raise ValueError(
                "No rows collected from api"
                f"Message: {data['message']}"
                f"Status: {data['status']}"
            )
        return rows

    async def get_fresh_news(self):
        """
        :return: saves last 20 news
        """
        return await self.get_news(limit=20)

    async def get_news(self, limit: int = 10) -> str:
        response = await self.session.get(
            url=self.url_unformatted.format(limit)
        )
        self.check_response(response)
        rows = self.check_return_data(response)
        response.close()

        filename = f"{self.ticker}_nasdaq_news_{limit}.json"
        await self._save_file(filename, rows, as_json=True)
        return filename
