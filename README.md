# bot

Using Telegram Bot API to create a bot that can send messages to a group.

Features:

- fetch and sent hot news from hacker news

## setup

### create a bot

1. talk to @BotFather
2. create a new bot
3. copy the token
4. create a file named `.env` in the root directory of this project
5. paste the token into the file with parameter `TELEGRAM_TOKEN=`

### create a group (if needed)

1. create a group
2. add the bot to the group
3. make the bot an admin of the group
4. get chat id of the group as described in the next section
5. paste the chat id into the `.env` file with parameter `TELEGRAM_GROUP_CHAT_ID=`

### set environment variables

```shell
cp .env.example .env
```

And set the values.

## run the bot

Using python 3.13

```shell
poetry install
```

```shell
# Development
poetry run python -m flask run --debug

# Production
poetry run gunicorn app:app
```

## Bot method

### get bot status

```python
from bot import Bot
Bot().is_active()
```

### send message

```python
from bot import Bot
Bot().send_message(chat_id=123, text='hello world')
```

### get group chat id of the first group

bot has to be an admin of the group.

```python
from bot import Bot
chat_id = Bot().get_first_group_chat_id()
```

## News method

### hot stories

```python
from news import News
News().hot_news()
```

as default, cache will be used to avoid too many requests to the server.

if bypass cache, set `bypass_cache=True`

```python
from news import News
News().hot_news(bypass_cache=False)
```

## Run

Fetch hot news and send to a chat group.

### Run by command

### Run App

production

```shell
gunicorn app:app
```

development

```shell
python -m flask run --debug
```

#### Endpoints

#### POST `/`

send message to a chat group

body parameters:

- `message`: message text. required.

#### POST `/news`

fetch hot news from hacker news and send to a chat group

body parameters: None

## Linter

### black

format as PEP8

```shell
black .
```

### isort

import order

```shell
isort .
```
