# SakuraTranslateBot

SakuraTranslateBot is a Telegram tool that automatically translates Chinese messages into Japanese.

It is useful for Japanese learning because it lets you write Chinese naturally and immediately compare it with a Japanese translation in the same Telegram message.

Although the project name contains `Bot`, this project is **not** a Telegram BotFather bot. It does not use a Telegram bot account. Instead, it uses your own Telegram account through Telegram API ID / API Hash and edits your outgoing messages.

## What It Does

When you send a Chinese message in Telegram, `userbot.py` detects your outgoing message, translates it into Japanese, and edits the original message so the Japanese translation appears under the Chinese text.

Example:

```text
小龙虾给我做的
> ザリガニが私に作ってくれたんだ
```

## Telegram API Configuration

This project requires a Telegram API application, not a BotFather bot.

Create one here:

```text
https://my.telegram.org/apps
```

Suggested values:

```text
App title: SakuraTranslateBot
Short name: sakuratranslatebot
Platform: Desktop
URL: leave empty
Description: A Chinese-to-Japanese translation tool for Telegram and Japanese learning.
```

After creating the application, Telegram will show:

```env
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
```

These values are required in your `.env` file.

## Model API Configuration

SakuraTranslateBot uses an OpenAI-compatible chat completion API.

The current recommended setup uses Google Gemini:

```env
LLM_API_KEY=your_model_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
```

You can use another OpenAI-compatible provider by changing `LLM_BASE_URL`, `LLM_MODEL`, and `LLM_API_KEY`.

## `.env` Setup

Copy the example file:

```bash
cp .env.example .env
```

Then edit `.env`:

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

Important:

- Do not commit `.env`.
- Do not commit `*.session` files.
- The session file stores your Telegram login state and should be treated like a password.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Run the user client mode:

```bash
source .venv/bin/activate
python userbot.py
```

On the first run, Telegram will ask for:

1. Your phone number.
2. The login code sent by Telegram.
3. Your two-step verification password, if enabled.

After login, a local session file will be created. Future runs usually do not require logging in again.

## Notes

- Only Chinese messages are translated.
- Non-Chinese messages are ignored.
- Slash commands are ignored.
- The translation output is Japanese only.
- Emoji and emoticons are not added to the translation.
