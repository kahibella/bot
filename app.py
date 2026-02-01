from flask import Flask
from flask import request
from flask_injector import FlaskInjector

from bot import Bot
from module import AppModule
from news import News
from use_case import send_message
from use_case import send_hot_news
from models import Result
from models.result import ResultStatus

app = Flask(__name__)


@app.route("/", methods=["POST"])
def message(bot: Bot) -> tuple[dict[str, str], int]:
    """
    Bot endpoint to send message to a chat group.
    body: {"message": "<text>"}
    """
    message_ = request.form.get("message", None)
    if message_ is None:
        return {"message": "No message"}, 400
    result: Result = send_message(bot=bot, message=message_)
    if result.status == ResultStatus.OK:
        return result.payload or {}, 200
    return result.payload or {}, 500


@app.route("/news", methods=["POST"])
def hot_news(bot: Bot, news: News) -> tuple[dict[str, str], int]:
    """
    Hot news endpoint to fetch hot news from hacker news and send to a chat group.
    """
    result: Result = send_hot_news(
        bot=bot,
        news=news,
    )
    if result.status == ResultStatus.OK:
        return result.payload or {}, 200
    return result.payload or {}, 500


FlaskInjector(app=app, modules=[AppModule()])
