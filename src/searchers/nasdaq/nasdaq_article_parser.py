from bs4 import BeautifulSoup


class NasdaqArticleParser:
    CSS_SELECTOR = ("body > div.dialog-off-canvas-main-canvas > div > main > "
                    "div.page__content > article > "
                    "div.nsdq-article-container.nsdq-c-band.nsdq-u-"
                    "padding-top-none.nsdq-u-padding-bottom-none.nsdq-u-"
                    "margin-bottom-lg > div.nsdq-l-layout-container--narrow."
                    "nsdq-l-layout-container.nsdq-u-padding-top-lg.nsdq-"
                    "u-padding-bottom-xl > "
                    "div > div.syndicated-article-main-body.nsdq-l-grid__item >"
                    " div.syndicated-article-body-wrapper.nsdq-l-grid.nsdq-l-grid"
                    "--2up-sr-left > div.layout__region.nsdq-l-grid__item."
                    "syndicated-article-body > section > div > div")

    def __int__(self, data: str):
        self.soup = BeautifulSoup(data)

    def parse(self) -> str:
        # body > div.dialog-off-canvas-main-canvas > div > main > div.page__content > article > div.nsdq-article-container.nsdq-c-band.nsdq-u-padding-top-none.nsdq-u-padding-bottom-none.nsdq-u-margin-bottom-lg > div.nsdq-l-layout-container--narrow.nsdq-l-layout-container.nsdq-u-padding-top-lg.nsdq-u-padding-bottom-xl > div > div.syndicated-article-main-body.nsdq-l-grid__item > div.syndicated-article-body-wrapper.nsdq-l-grid.nsdq-l-grid--2up-sr-left > div.layout__region.nsdq-l-grid__item.syndicated-article-body > section > div > div
        body = self.soup.select_one(self.CSS_SELECTOR)
        return body.text
