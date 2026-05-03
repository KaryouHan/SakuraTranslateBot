# SakuraTranslateBot

SakuraTranslateBot automatically translates outgoing Chinese Telegram messages into Japanese and appends the translation under the original message.

It is designed for daily Telegram conversations and Japanese learning. You can write naturally in Chinese, then compare your sentence with a Japanese translation right away.

## Features

- Detects outgoing Chinese messages in Telegram.
- Translates Chinese into Japanese with a configurable model API.
- Edits the original Telegram message and adds the Japanese translation below it.
- Ignores non-Chinese messages and slash commands.
- Keeps the translation output clean without extra emoji or emoticons.

Example output:

```text
小龙虾给我做的
> ザリガニが私に作ってくれたんだ
```

## Requirements

- Python 3.10+
- Telegram API ID and API Hash
- A model API key, such as Google Gemini or another OpenAI-compatible provider

## Telegram API ID / API Hash

Create a Telegram API application here:

```text
https://my.telegram.org/apps
```

Suggested values:

```text
App title: SakuraTranslateBot
Short name: sakuratranslatebot
Platform: Desktop
URL: leave empty
Description: Chinese-to-Japanese translation tool for Telegram and Japanese learning.
```

After creating the application, copy these values:

```env
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
```

## Model API Configuration

SakuraTranslateBot uses an OpenAI-compatible chat completion API.

Default Gemini example:

```env
LLM_API_KEY=your_model_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
```

You can use a different OpenAI-compatible provider by changing:

```env
LLM_API_KEY=
LLM_BASE_URL=
LLM_MODEL=
```

## Installation

```bash
git clone https://github.com/KaryouHan/SakuraTranslateBot.git
cd SakuraTranslateBot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## `.env` Setup

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
LLM_API_KEY=your_model_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
SOURCE_LANGUAGE=Chinese
TARGET_LANGUAGE=Japanese
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_SESSION_NAME=sakura_translate
```

## Run

```bash
source .venv/bin/activate
python userbot.py
```

On the first run, Telegram asks for your phone number and login code. If two-step verification is enabled, it will also ask for your password.

After login, SakuraTranslateBot starts watching outgoing Telegram messages. Send a Chinese message in Telegram and the Japanese translation will be added under it automatically.

## Configuration Reference

| Variable | Description |
| --- | --- |
| `LLM_API_KEY` | API key for the model provider |
| `LLM_BASE_URL` | OpenAI-compatible API base URL |
| `LLM_MODEL` | Model name used for translation |
| `SOURCE_LANGUAGE` | Source language, default `Chinese` |
| `TARGET_LANGUAGE` | Target language, default `Japanese` |
| `TELEGRAM_API_ID` | Telegram API application ID |
| `TELEGRAM_API_HASH` | Telegram API application hash |
| `TELEGRAM_SESSION_NAME` | Local Telegram session name |
