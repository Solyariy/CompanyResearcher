import json
import os


URL_FOR_MAPPINGS = "https://www.sec.gov/files/company_tickers.json"

def get_cik(ticker: str) -> str | None:
    file_dir = os.path.dirname(__file__)
    path = os.path.join(file_dir, "cik_mapping.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data.get(ticker)