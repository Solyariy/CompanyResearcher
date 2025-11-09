import curl_cffi as cff



class NasdaqArticleScraper:
    def __init__(self, session: cff.AsyncSession, url: str):
        self.session = session
        self.url = url

    def check_response(self, response):
        if response.status_code != 200:
            raise ValueError(
                f"NasdaqArticleScraper response code: {response.status_code}, "
                f"reason: {response.reason} "
                f"for url: {self.url}"
            )

    async def get_article(self, url: str) -> str:
        res = await self.session.get(url, impersonate="chrome")
        self.check_response(res)
        data = res.content
        res.close()
        return data
