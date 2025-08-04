import os
from pathlib import Path

from selenium_driverless.webdriver import Chrome, ChromeOptions

FILEPATH = os.path.join(Path(__file__).resolve().parent, "test_files")

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
