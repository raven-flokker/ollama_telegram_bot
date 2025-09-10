import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from services.ollama import client  # Импортируем клиент

# Импортируем роутеры
from handlers import start, message, inline, clear, context


async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Бот и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start.router)  # Команда старт
    dp.include_router(clear.router)  # Команда очистка контекста
    dp.include_router(context.router)  # Команда просмотра сохраненного контекста
    dp.include_router(message.router)  # Хендлер отлова команды мяу
    dp.include_router(inline.router)  # Отлов инлайн

    # Запуск
    logging.info("Бот запущен...")
    try:
        await dp.start_polling(bot)
    finally:
        await client.aclose()  # Закрываем HTTP-клиент


if __name__ == "__main__":
    asyncio.run(main())
