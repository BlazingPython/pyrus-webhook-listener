from fastapi import APIRouter, Request, BackgroundTasks
import logging
from .security import validate_webhook_signature

router = APIRouter()
logger = logging.getLogger("pyrus_webhook")


def is_task_valid(task_info: dict) -> bool:
    """Возвращает True, если комментарии отсутствуют, иначе False"""
    return True if not task_info.get("comments") else False

async def process_webhook(data: dict):
    """Асинхронная обработка вебхука в фоне"""
    task_data = data.get('task')
    is_valid = is_task_valid(task_data)
    if not is_valid:
        logger.info("Задача не подходит")
        return

    logger.info(task_data)


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