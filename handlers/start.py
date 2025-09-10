from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message):
    await message.answer("Привет! Используй Мяу <вопрос>, чтобы задать вопрос котику.")
