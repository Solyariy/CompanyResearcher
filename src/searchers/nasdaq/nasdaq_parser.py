import pandas as pd
from src.searchers.utils.scripts import get_path_to_files


class NasdaqParser:
    def __int__(self, filename: str):
        self._filename = filename
        self.filepath = get_path_to_files(filename)

    def parse(self) -> pd.DataFrame:
        df = pd.read_json(self.filepath)
        df["date"] = pd.to_datetime(df["created"])
        df = df.drop(columns=["image", "ago", "primarytopic", "imagedomain", "created"])
        return df
