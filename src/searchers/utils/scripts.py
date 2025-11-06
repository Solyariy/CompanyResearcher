import json
import os
from typing import Any
from urllib.robotparser import RobotFileParser
from src.base_config import FILEPATH


# URL_FOR_MAPPINGS = "https://www.sec.gov/files/company_tickers.json"


def get_cik(ticker: str) -> str | None:
    file_dir = os.path.dirname(__file__)
    path = os.path.join(file_dir, "cik_mapping.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data.get(ticker, ticker)


def parse_robot_file(domain: str, url_to_check: str) -> dict[str, Any]:
    parser = RobotFileParser()
    parser.set_url(f"https://{domain}/robots.txt")
    user_agent = "*"
    return {
        "can_fetch": parser.can_fetch(user_agent, url_to_check),
        "request_rate": parser.request_rate(user_agent)
    }


def load_json(filename: str):
    filepath = os.path.join(FILEPATH, filename)
    with open(filepath, "r") as f:
        return json.load(f)
