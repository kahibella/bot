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
    """Bot endpoint.
    body: {"message": "<text>"}
    """
    message_ = request.form.get("message", None)
    if message_ is None:
        return {"message": "No message"}, 400
    result: Result = send_message(bot=bot, message=message_)
    if result.status == ResultStatus.OK:
        return result.payload or {}, 200
    return result.payload or {}, 500


@app.route("/news", methods=["GET"])
def hot_news(bot: Bot, news: News) -> tuple[dict[str, str], int]:
    """Hot news endpoint."""
    points_threshold = request.args.get("points", None, type=int)
    created_at_threshold_sec = request.args.get("created_at", None, type=int)

    result: Result = send_hot_news(
        bot=bot,
        news=news,
        points_threshold=points_threshold,
        created_at_threshold_sec=created_at_threshold_sec,
    )
    if result.status == ResultStatus.OK:
        return result.payload or {}, 200
    return result.payload or {}, 500


FlaskInjector(app=app, modules=[AppModule()])
