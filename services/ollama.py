import requests
from config import OLLAMA_URL, MODEL_NAME
from services.prompts import SYSTEM_PROMPT
from services.memory import add_message, get_context
import logging
import httpx

logger = logging.getLogger(__name__)

# Создаём клиент один раз.
# Приблуды для ускорения и отсутствия проблемы когда бот висит от одного запроса.
client = httpx.AsyncClient(
    base_url=OLLAMA_URL,
    timeout=httpx.Timeout(60.0)
)


async def ask_llm(user_id: int, prompt: str) -> str:  # с использованием контекста по user_id
    logging.info(f"[Ollama] Запрос от user_id={user_id}: {prompt}")
    try:
        # Добавляем запрос пользователя
        add_message(user_id, "user", prompt)

        # Получаем полный контекст
        context = get_context(user_id)

        # response = requests.post(
        response = await client.post(
            # f"{OLLAMA_URL}/api/generate",
            "/api/chat",  # Обязательно chat для контекста
            json={
                "model": MODEL_NAME,
                "messages": context,
                # "prompt": prompt,
                # "system": SYSTEM_PROMPT,
                "stream": False,
                "think": False,  # Это точно выключает мышление (вывод размышления)
                "role": "assistant",
                "options": {
                    "temperature": 0.8,  # Баланс креативности и стабильности 0.8 дефолт
                    "top_p": 0.9,
                    "repeat_penalty": 1.1,
                    "num_predict": 1000,  # Макс. длина ответа
                    "nothink": True,  # Скорее не работает
                    "think": False  # Скорее не работает

                }
            },
            # timeout=30
        )
        response.raise_for_status()
        # return response.json()["response"].strip()
        answer = response.json()["message"]["content"].strip()

        # Сохраняем ответ
        add_message(user_id, "assistant", answer)
        logging.info(f"[Ollama] Ответ: {answer[:50]}...")
        return answer
    except requests.exceptions.RequestException as e:
        print(f"[Ollama] Error: {e}")
        logging.error(f"[Ollama] Ошибка: {e}")
        # return "Кажется котик умер. Мы уже работаем над его воскрешением."
        # Удаляем последний user-сообщение, чтобы не сломать контекст
        try:
            ctx = get_context(user_id)
            if len(ctx) > 1 and ctx[-1]["role"] == "user":
                ctx.pop()
                from services.memory import save_context
                save_context(user_id, ctx)
        except:
            pass
        return "Мяу. Я потерял мысль. Повтори? 🤔"
