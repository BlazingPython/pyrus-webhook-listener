from fastapi import APIRouter, Request, BackgroundTasks
import logging
from .security import validate_webhook_signature

router = APIRouter()
logger = logging.getLogger("pyrus_webhook")


async def process_webhook(data: dict):
    """Асинхронная обработка вебхука в фоне"""
    logger.info(f"Received Pyrus event: {data['event']}")
    logger.info(f"Task ID: {data['task_id']}")
    logger.info(f"User ID: {data['user_id']}")
    logger.info(f"Task details: {data.get('task')}")
    # Здесь будет основная логика обработки


@router.post("/pyrus-webhook")
async def handle_webhook(
        request: Request,
        background_tasks: BackgroundTasks
):
    # Проверка подписи
    await validate_webhook_signature(request)

    # Извлекаем данные
    data = await request.json()
    retry_header = request.headers.get("X-Pyrus-Retry", "1/3")

    logger.info(f"Incoming webhook (attempt {retry_header})")
    background_tasks.add_task(process_webhook, data)

    return {"status": "ok"}  # Pyrus требует 2xx ответ