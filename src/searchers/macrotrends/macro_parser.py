import os.path
from typing import Any

import numpy as np
import pandas as pd
from src.base_config import FILEPATH
from src.searchers.utils.scripts import load_json


class MTParser:
    def __init__(self, filename: str):
        self._filename = filename
        self.filepath = os.path.join(FILEPATH, filename)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self.filepath = os.path.join(FILEPATH, value)

    def parse(self) -> pd.DataFrame:
        if self.filename.split(".")[-1] == "csv":
            return self.parse_price_history()
        return self.parse_all_stock_analysis()

    def parse_price_history(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        return df

    def parse_all_stock_analysis(self) -> pd.DataFrame:
        data = load_json(self.filename)
        df = self.__to_dataframe(data)
        return df

    @staticmethod
    def __to_dataframe(data: list[dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df = df.map(MTParser._convert_types)
        return df

    @staticmethod
    def _convert_types(entry: str):
        if not entry:
            return np.nan
        if entry.isnumeric():
            return float(entry)
        return entry
