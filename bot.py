import json
import logging
import os
import re
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import AsyncOpenAI
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


CHINESE_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
TELEGRAM_MESSAGE_LIMIT = 4096
BOT_NAME = "SakuraTranslateBot"


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    source_language: str
    target_language: str
    reply_mode: str


def load_settings() -> Settings:
    load_dotenv()

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    llm_api_key = os.getenv("LLM_API_KEY", "").strip()

    missing = []
    if not telegram_bot_token:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not llm_api_key:
        missing.append("LLM_API_KEY")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return Settings(
        telegram_bot_token=telegram_bot_token,
        llm_api_key=llm_api_key,
        llm_base_url=os.getenv(
            "LLM_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta/openai/",
        ).strip(),
        llm_model=os.getenv("LLM_MODEL", "gemini-2.5-flash-lite").strip(),
        source_language=os.getenv("SOURCE_LANGUAGE", "Chinese").strip(),
        target_language=os.getenv("TARGET_LANGUAGE", "Japanese").strip(),
        reply_mode=os.getenv("BOT_REPLY_MODE", "paired").strip().lower(),
    )


def contains_chinese(text: str) -> bool:
    return bool(CHINESE_RE.search(text))


def split_sentences(text: str) -> list[str]:
    normalized = re.sub(r"\n{3,}", "\n\n", text.strip())
    if not normalized:
        return []

    pieces = re.split(r"(?<=[。！？!?；;])\s+|\n+", normalized)
    return [piece.strip() for piece in pieces if piece.strip()]


async def translate_sentences(client: AsyncOpenAI, settings: Settings, sentences: list[str]) -> list[str]:
    response = await client.chat.completions.create(
        model=settings.llm_model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful translator for Telegram chats. "
                    f"Translate from {settings.source_language} to {settings.target_language}. "
                    "Preserve casual tone, names, slang, emoji, numbers, and line meaning. "
                    "Return only valid JSON in the shape {\"translations\": [\"...\"]}. "
                    "The translations array must have exactly the same length and order as the input array."
                ),
            },
            {
                "role": "user",
                "content": json.dumps({"sentences": sentences}, ensure_ascii=False),
            },
        ],
    )

    content = response.choices[0].message.content or ""
    data = json.loads(content)
    translations = data.get("translations")
    if not isinstance(translations, list) or len(translations) != len(sentences):
        raise ValueError("Translator returned an unexpected response shape.")

    return [str(item).strip() for item in translations]


def format_reply(sentences: list[str], translations: list[str], reply_mode: str) -> str:
    if reply_mode == "translation_only":
        return "\n".join(translations)

    blocks = []
    for source, translated in zip(sentences, translations):
        blocks.append(f"{source}\n{translated}")
    return "\n\n".join(blocks)


def chunk_message(text: str, limit: int = TELEGRAM_MESSAGE_LIMIT) -> list[str]:
    chunks = []
    current = ""

    for block in text.split("\n\n"):
        separator = "\n\n" if current else ""
        candidate = f"{current}{separator}{block}"
        if len(candidate) <= limit:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        while len(block) > limit:
            chunks.append(block[:limit])
            block = block[limit:]
        current = block

    if current:
        chunks.append(current)

    return chunks


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text(f"{BOT_NAME} 已启动。发中文给我，我会把它翻译成日语回复在下面。")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text(
            "直接发送中文即可翻译成日语。群聊里如果我没有反应，请在 BotFather 里关闭 Group Privacy。"
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    if not contains_chinese(text):
        return

    settings: Settings = context.application.bot_data["settings"]
    client: AsyncOpenAI = context.application.bot_data["llm_client"]
    sentences = split_sentences(text)
    if not sentences:
        return

    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        translations = await translate_sentences(client, settings, sentences)
        reply = format_reply(sentences, translations, settings.reply_mode)
    except Exception:
        logging.exception("Failed to translate message")
        reply = "翻译时出错了，稍后再试一下。"

    for chunk in chunk_message(reply):
        await update.message.reply_text(chunk)


async def post_init(application: Application) -> None:
    settings: Settings = application.bot_data["settings"]
    me = await application.bot.get_me()
    logging.info("%s is running as @%s with model %s", BOT_NAME, me.username, settings.llm_model)


def build_application(settings: Settings) -> Application:
    application = Application.builder().token(settings.telegram_bot_token).post_init(post_init).build()
    application.bot_data["settings"] = settings
    application.bot_data["llm_client"] = AsyncOpenAI(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    return application


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    settings = load_settings()
    application = build_application(settings)
    print(f"{BOT_NAME} is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
