from aiogram import Router, types, F
from services.ollama import ask_llm
from utils.helpers import random_greeting

router = Router()


# Команда вызова вопроса. "Мяу как дела?" Можно поменять на свое
@router.message(F.text.lower().startswith("мяу"))
async def handle_message(message):
    user_id = message.from_user.id
    # if message.text and message.text.strip().lower().startswith("мяу"):
    prompt = message.text.strip()[3:].strip()

    if not prompt:
        await message.reply(random_greeting())
        return

    answer = await ask_llm(user_id, prompt)
    await message.reply(answer)
