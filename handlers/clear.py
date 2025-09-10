from aiogram import Router
from aiogram.filters import Command
from services.memory import clear_context

router = Router()


@router.message(Command("clear"))
async def cmd_clear(message):
    clear_context(message.from_user.id)
    await message.reply("Мяу. Я всё забыл. 🤯")
