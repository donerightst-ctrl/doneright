import os
import sqlite3
from contextlib import closing

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from openai import AsyncOpenAI

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Ты полезный AI-ассистент. Отвечай кратко, точно и по делу.",
)
DB_PATH = os.getenv("DB_PATH", "chat_memory.sqlite3")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "12"))

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_history(user_id: int) -> list[dict[str, str]]:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, MAX_HISTORY),
        ).fetchall()
    return [
        {"role": role, "content": content}
        for role, content in reversed(rows)
    ]


def save_message(user_id: int, role: str, content: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content),
        )
        conn.commit()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Я AI-бот с памятью диалога. Напиши сообщение — я отвечу и запомню контекст."
    )


@dp.message(F.text)
async def chat(message: Message) -> None:
    user_id = message.from_user.id
    user_text = message.text.strip()
    save_message(user_id, "user", user_text)

    history = get_history(user_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history]

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        answer = response.choices[0].message.content or "Не удалось сформировать ответ."
    except Exception:
        await message.answer("Временная ошибка AI-сервиса. Попробуйте ещё раз чуть позже.")
        return

    save_message(user_id, "assistant", answer)
    await message.answer(answer)


async def main() -> None:
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
