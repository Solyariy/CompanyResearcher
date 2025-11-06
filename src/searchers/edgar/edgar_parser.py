from typing import Any

import pandas as pd
from src.searchers.utils.scripts import load_json

class EdgarParser:
    def __init__(self, filename: str,  desired_keys: list[str] | None = None):
        self.filename = filename
        self.desired_keys = desired_keys or [
            "GrossProfit", "OperatingIncomeLoss", "NetIncomeLoss",
            "Assets", "Liabilities", "StockholdersEquity",
            "NetCashProvidedByUsedInOperatingActivities",
            "PaymentsToAcquirePropertyPlantAndEquipment"
        ]

    def parse(self) -> pd.DataFrame:
        data = load_json(self.filename)["facts"]["us-gaap"]
        all_metrics_data = []
        for key in self.desired_keys:
            metric = data.get(key)
            if metric is None:
                raise KeyError(f"key {key} not found in {data.keys()}")
            description = metric["description"]
            label = metric["label"]
            for entry in metric["units"]["USD"]:
                record = {
                    "Metric": key,
                    "Label": label.strip(),
                    "Description": description.strip(),
                    "Value": entry.get("val"),
                    "Date": entry.get("end"),
                    "Form": entry.get("form"),
                    "Period": entry.get("fp"),
                    "FiscalYear": entry.get("fy")
                }
                all_metrics_data.append(record)
        return self.__to_dataframe(all_metrics_data)

    @staticmethod
    def __to_dataframe(data: list[dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df = df.dropna(subset=["Value", "Date"])
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values(by=["Date"], ascending=True)
        return df
