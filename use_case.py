from bot import Bot
from models import Result
from models.result import ResultStatus
from news import News


def send_message(bot: Bot, message: str) -> Result:
    group_chat_id = bot.group_chat_id()
    if group_chat_id is None:
        print("No group chat id.")
        return Result(status=ResultStatus.ERROR, payload={"message": "No group chat id"})

    bot.send_message(chat_id=group_chat_id, text=message)
    return Result(status=ResultStatus.OK, payload={"message": message})


def send_hot_news(
    bot: Bot,
    news: News,
) -> Result:
    """
    Fetch hot news from hacker news and send to a chat group.
    :param bot: Bot instance
    :param news: News instance
    :return: Result instance
    """
    hot_news = news.hot_news(
        bypass_cache=True,
    )
    if not hot_news.has_result():
        print("No result.")
        return Result(status=ResultStatus.OK, payload={"message": "No result"})

    group_chat_id = bot.group_chat_id()
    if group_chat_id is None:
        print("No group chat id.")
        return Result(status=ResultStatus.ERROR, payload={"message": "No group chat id"})

    if len(hot_news.hits) == 0:
        print("No hits.")
        return Result(status=ResultStatus.OK, payload={"message": "No hits"})

    for hit in hot_news.hits:
        bot.send_message(chat_id=group_chat_id, text=hit.to_text())
    return Result(status=ResultStatus.OK, payload={"message": hot_news.to_dict()})
