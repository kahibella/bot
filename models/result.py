from dataclasses import dataclass
from typing import Any
from enum import Enum


class ResultStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


@dataclass
class Result:
    status: ResultStatus
    payload: dict[str, Any] | None = None
