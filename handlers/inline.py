from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
import uuid

from config import THUMBNAIL_URL
from services.ollama import ask_llm

router = Router()


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    try:
        user_id = inline_query.from_user.id
        query_text = inline_query.query.strip()

        if not query_text:
            return

        answer = await ask_llm(user_id, query_text)
        result_id = str(uuid.uuid4())

        item = InlineQueryResultArticle(
            id=result_id,
            title="Спросить котика-гения",
            input_message_content=InputTextMessageContent(message_text=answer),
            description=f"Вопрос: {query_text[:50]}..." if len(query_text) > 50 else query_text,
            thumbnail_url=THUMBNAIL_URL,
            thumbnail_width=48,
            thumbnail_height=48
        )

        await inline_query.answer([item], cache_time=5)
    except Exception as e:
        print(f"[Inline] Error: {e}")
