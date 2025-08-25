import json
import os
from abc import ABC
from pathlib import Path

import aiofiles


class BaseScraper(ABC):
    FILEPATH = os.path.join(
        Path(__file__).resolve().parent.parent,
        "test_files"
    )

    @staticmethod
    async def _save_file(
            filename: str,
            data: bytes | str,
            /,
            is_binary: bool = False,
            as_json: bool = False
    ) -> None:
        mode = "wb" if is_binary else "w"
        filepath = os.path.join(BaseScraper.FILEPATH, filename)
        data = data if not as_json else json.dumps(data)
        async with aiofiles.open(filepath, mode) as f:
            await f.write(data)
