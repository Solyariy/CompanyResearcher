from typing import Any
import pandas as pd

class EdgarParser:
    def __init__(self, data: dict[str, Any], desired_keys: list[str] | None = None):
        self.data = data
        if desired_keys:
            self.desired_keys = desired_keys
        else:
            self.desired_keys = [
                "GrossProfit", "OperatingIncomeLoss", "NetIncomeLoss",
                "Assets", "Liabilities", "StockholdersEquity",
                "EarningsPerShareBasic", "NetCashProvidedByUsedInOperatingActivities",
                "PaymentsToAcquirePropertyPlantAndEquipment"
            ]

    def parse(self) -> pd.DataFrame:
        descriptions = {}
        all_metrics_data = []
        for key in self.desired_keys:
            try:
                metric = self.data[key]
                descriptions[key] = metric["description"]
                for entry in metric["units"]["USD"]:
                    record = {
                        "Metric": key,
                        "Value": entry.get("val"),
                        "Date": entry.get("end"),
                        "Form": entry.get("form"),
                        "Period": entry.get("fp"),
                        "FiscalYear": entry.get("fy")
                    }
                    all_metrics_data.append(record)
            except KeyError as e:
                print(f"key {e} not found in {key}")
        return self.__to_dataframe(all_metrics_data)

    @staticmethod
    def __to_dataframe(data: list[dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df = df.dropna(subset=["Value", "Date"])
        df["Date"] = pd.to_datetime(df["Date"])
        df["FiscalYear"] = df["FiscalYear"].astype(int)
        df = df.sort_values(by=["Date"], ascending=True)
        return df

