from aiogram import Router, F
from aiogram.filters import Command
from services.memory import get_context

router = Router()


@router.message(Command("context"))
async def cmd_context(message):
    context = get_context(message.from_user.id)

    # Убираем system-сообщение — оно не для пользователей
    chat_history = [msg for msg in context if msg["role"] != "system"]

    if not chat_history:
        await message.reply("Мяу. Я ничего не помню. 🤯")
        return

    # Форматируем последние N сообщений (например, 10)
    lines = ["📝 *Последние сообщения в памяти:*", ""]
    for msg in chat_history[-10:]:  # Покажем максимум 10
        if msg["role"] == "user":
            lines.append(f"🟢 *Ты:* {msg['content']}")
        elif msg["role"] == "assistant":
            lines.append(f"🔵 *Котик:* {msg['content']}")

    await message.reply("\n".join(lines), parse_mode="Markdown")
