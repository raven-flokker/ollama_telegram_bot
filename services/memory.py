import redis
import json
from typing import List, Dict
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, CONTEXT_TTL, MAX_MESSAGES

# Подключение к Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Константы
CONTEXT_KEY_PREFIX = "chat_context:"
TTL = CONTEXT_TTL  # 3600 сек = 1 час


def get_context(user_id: int) -> List[Dict]:
    key = f"{CONTEXT_KEY_PREFIX}{user_id}"
    data = r.get(key)
    if data:
        r.expire(key, TTL)  # Обновляем TTL при каждом доступе
        return json.loads(data)
    return []


def save_context(user_id: int, context: List[Dict]):
    key = f"{CONTEXT_KEY_PREFIX}{user_id}"
    r.setex(key, TTL, json.dumps(context, ensure_ascii=False))


def add_message(user_id: int, role: str, content: str):
    context = get_context(user_id)

    # Если контекста нет — добавим system-промпт
    if not context:
        from services.prompts import SYSTEM_PROMPT
        context = [{"role": "system", "content": SYSTEM_PROMPT}]

    context.append({"role": role, "content": content})

    # Ограничиваем длину: system + последние N
    if len(context) > MAX_MESSAGES + 1:
        context = [context[0]] + context[-MAX_MESSAGES:]

    save_context(user_id, context)


def clear_context(user_id: int):
    key = f"{CONTEXT_KEY_PREFIX}{user_id}"
    r.delete(key)
