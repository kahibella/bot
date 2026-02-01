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

## run the bot

Using python 3.13

```shell
poetry install
```

```shell
poetry run python app.py
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

#### GET `/news`

fetch hot news from hacker news and send to a chat group

query parameters:

- `points`: points threshold. optional. default is 200.
- `created_at`: created at threshold. optional. default is 12 hours.

## Deploy to Cloudflare Workers

This project includes a `worker.py` file that allows deployment to Cloudflare Workers.

### Prerequisites

1. Install Wrangler CLI:

```shell
npm install -g wrangler
```

2. Login to Cloudflare:

```shell
wrangler login
```

### Setup Environment Variables

Set your secrets using Wrangler:

```shell
wrangler secret put TELEGRAM_TOKEN
# Enter your Telegram bot token when prompted

wrangler secret put TELEGRAM_GROUP_CHAT_ID
# Enter your Telegram group chat ID when prompted
```

### Deploy Steps

1. Generate requirements.txt:

```shell
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

2. Deploy to Cloudflare Workers:

```shell
wrangler deploy
```

### Worker Endpoints

The Worker provides the same API as the Flask app:

- **POST /** - Send message to chat group (form data: `message`)
- **POST /news** - Fetch and send hot news (JSON body: `points`, `created_at`)

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
