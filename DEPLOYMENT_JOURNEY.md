# SakuraTranslateBot Deployment Journey

SakuraTranslateBot is a personal Telegram automation project that automatically translates Chinese messages into Japanese. It is designed for bilingual chat workflows and for learning Japanese by seeing a Japanese translation directly under the original Chinese sentence.

## Project Goal

The original goal was to reproduce a Telegram message style where a Chinese sentence appears first and a Japanese translation appears below it in a Telegram quote-style block.

Example target behavior:

```text
小龙虾给我做的
> ザリガニが私に作ってくれたんだ
```

Instead of sending a separate reply message, the final implementation edits the outgoing message from the user's own Telegram account and appends the Japanese translation below the Chinese original.

## Why a Normal Telegram Bot Was Not Enough

At first, the project was implemented as a standard Telegram bot created with BotFather. That version could receive Chinese messages and reply with Japanese translations.

However, a standard Telegram bot has important limitations:

- It cannot monitor every message sent by a personal Telegram account.
- It cannot edit messages sent by the user's own account.
- It only works in chats where the bot is present.
- In groups, it may require BotFather privacy mode changes to read regular messages.

Because the desired behavior was to modify the user's own outgoing messages, the project changed from a normal bot into a Telegram user client automation using Telethon.

## Final Architecture

The final setup uses:

- Telegram API ID and API Hash for personal account login.
- Telethon to listen for outgoing messages from the user's Telegram account.
- Google Gemini API through an OpenAI-compatible endpoint.
- Python dotenv configuration through a local `.env` file.

Flow:

1. The user sends a Chinese message in Telegram.
2. `userbot.py` detects the outgoing message.
3. The text is sent to Gemini for Chinese-to-Japanese translation.
4. The original Telegram message is edited.
5. The edited message keeps the Chinese text and appends the Japanese translation in a quote-style block.

## Telegram Configuration

### BotFather Bot

A BotFather bot was created during the first phase, but it is no longer required for the final behavior.

The normal bot mode still exists in `bot.py` for reference, but the main implementation is `userbot.py`.

### Telegram API Application

To enable personal account automation, a Telegram API application was created at:

```text
https://my.telegram.org/apps
```

Suggested application settings:

```text
App title: SakuraTranslateBot
Short name: sakuratranslatebot
Platform: Desktop
URL: leave empty
Description: A personal Telegram translation assistant that automatically translates outgoing Chinese messages into Japanese and helps users learn Japanese.
```

After creation, Telegram provides:

```text
TELEGRAM_API_ID
TELEGRAM_API_HASH
```

These values are required by `userbot.py`.

## Google Gemini API Configuration

The project originally used DeepSeek API, but it was later migrated to Google Gemini because the user wanted an overseas API provider with fewer concerns around Chinese political content restrictions.

The current Gemini configuration uses Google's OpenAI-compatible API endpoint:

```env
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
```

A Gemini API key is required:

```env
LLM_API_KEY=your_google_gemini_api_key
```

The old DeepSeek configuration has been removed from the project.

## Environment Variables

Create a local `.env` file based on `.env.example`:

```env
TELEGRAM_BOT_TOKEN=
LLM_API_KEY=your_google_gemini_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
SOURCE_LANGUAGE=Chinese
TARGET_LANGUAGE=Japanese
BOT_REPLY_MODE=paired
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_SESSION_NAME=sakura_translate
```

Important security notes:

- Do not commit `.env`.
- Do not commit `*.session` files.
- The Telethon session file stores Telegram login state and should be treated like a password.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Final User Mode

```bash
source .venv/bin/activate
python userbot.py
```

On first run, Telethon asks for:

1. Telegram phone number.
2. Telegram login code.
3. Two-step verification password, if enabled.

After login, a local session file is created, so future runs usually do not require another login code.

## Current Behavior

The final user mode:

- Watches outgoing Telegram messages.
- Ignores non-Chinese messages.
- Ignores slash commands.
- Sends Chinese text to Gemini.
- Edits the original message instead of sending a separate reply.
- Appends Japanese translation in Telegram blockquote style.
- Avoids adding emoji or emoticons to the translation output.
- Logs translation and Telegram edit latency.

## Learning Japanese Use Case

SakuraTranslateBot can be used as a lightweight Japanese learning assistant. By writing Chinese messages naturally and seeing the Japanese translation immediately below, the user can compare sentence structure, vocabulary, tone, and casual phrasing in real conversations.

This makes the tool useful not only for communication, but also for repeated exposure to practical Japanese.

## Rate Limit Notes

During testing, Google Gemini free-tier limits were reached. The error indicated a quota limit for `gemini-2.5-flash-lite` free-tier requests.

If this happens:

- Wait for the quota window to reset.
- Enable billing in Google AI Studio / Google Cloud.
- Try another compatible model if appropriate.
- Avoid repeatedly sending test messages while the API is rate-limited.

The code includes a cooldown behavior for Gemini rate limits to avoid repeated failed retries.

## Main Files

```text
userbot.py          Final personal Telegram account automation
bot.py              Earlier standard Telegram bot mode
requirements.txt    Python dependencies
.env.example        Safe example configuration
.gitignore          Secret and session exclusions
README.md           Project usage documentation
```

## Repository

GitHub repository:

```text
https://github.com/KaryouHan/SakuraTranslateBot
```
