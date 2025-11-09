import os
from pathlib import Path

from selenium_driverless.webdriver import Chrome, ChromeOptions
from src.base_config import FILEPATH


class ChromeEmulator(Chrome):
    def __init__(self, proxy: str = ""):
        if proxy:
            self.set_single_proxy(proxy)
        self._options = ChromeOptions()
        self.__set_options()
        super().__init__(options=self.options)

    def __set_options(self):
        self.options.update_pref(
            "download.default_directory", FILEPATH
        )

    @property
    def options(self):
        return self._options
