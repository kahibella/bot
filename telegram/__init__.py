import os
from typing import ClassVar
from typing import Type
from typing import TypeVar

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

from .results import GetMeResultModel
from .results import GetUpdatesResultModel
from .results import SendMessageResultModel

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class Telegram:
    __TOKEN: ClassVar[str] = os.getenv("TELEGRAM_TOKEN")
    __GROUP_CHAT_ID: ClassVar[int] = int(os.getenv("TELEGRAM_GROUP_CHAT_ID"))

    @property
    def group_chat_id(self) -> int | None:
        return self.__GROUP_CHAT_ID

    @staticmethod
    def parse_response(response: requests.Response, to_model: Type[T]) -> T:
        if 200 <= response.status_code < 300 or response.json()["ok"] is False:
            return to_model.model_validate(response.json()["result"])
        else:
            raise Exception(f"Error: {response.status_code}")

    def get_me(self) -> GetMeResultModel:
        request = requests.get(
            f"https://api.telegram.org/bot{self.__TOKEN}/getMe",
        )
        return self.parse_response(response=request, to_model=GetMeResultModel)

    def get_updates(self) -> GetUpdatesResultModel:
        # If result is empty array, add bot to group of an admin.
        request = requests.get(
            f"https://api.telegram.org/bot{self.__TOKEN}/getUpdates",
        )
        return self.parse_response(response=request, to_model=GetUpdatesResultModel)

    def send_message(self, chat_id: int, text: str) -> SendMessageResultModel:
        request = requests.post(
            f"https://api.telegram.org/bot{self.__TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
        )
        return self.parse_response(response=request, to_model=SendMessageResultModel)
