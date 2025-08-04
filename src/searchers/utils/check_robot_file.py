from typing import Any
from urllib.robotparser import RobotFileParser


def parse_robot(domain: str, url_to_check: str) -> dict[str, Any]:
    parser = RobotFileParser()
    parser.set_url(f"https://{domain}/robots.txt")
    user_agent = "*"
    can_fetch = parser.can_fetch(user_agent, url_to_check)
    request_rate = parser.request_rate(user_agent)
    return {
        "can_fetch": can_fetch,
        "request_rate": request_rate
    }
