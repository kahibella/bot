import json
import os
from datetime import UTC
from datetime import datetime
from typing import Any


class Cache:
    def __init__(self, directory: str):
        self.directory = directory

    @staticmethod
    def default_file_pref() -> str:
        now = datetime.now(tz=UTC)
        return f"{now.strftime('%Y%m%d%H%M')}"

    def latest_file_name(self) -> str | None:
        files = os.listdir(self.directory)
        if len(files) == 0:
            return None
        files.sort(reverse=True)
        latest_file = files[0]
        return latest_file

    def load_latest_json(self, expire_sec: int = None) -> dict[str, Any] | None:
        latest_file = self.latest_file_name()
        # FIXME(kahi0223): cannot convert if dir includes not json file
        latest_file_datetime = datetime.strptime(latest_file, "%Y%m%d%H%M.json")
        if expire_sec is not None:
            if (datetime.now() - latest_file_datetime).total_seconds() > expire_sec:
                return None
        with open(f"{self.directory}/{latest_file}", "r") as file:
            return json.load(file)

    def save_json(self, data: dict[str, Any], file_name: str = None) -> None:
        file_name = file_name or f"{self.default_file_pref()}.json"
        with open(f"{self.directory}/{file_name}", "x") as file:
            json.dump(data, file, indent=4)
