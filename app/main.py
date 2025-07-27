from fastapi import FastAPI
import logging
from .config import settings
from .webhooks import router as webhook_router

app = FastAPI(title="Pyrus Webhook Handler")
app.include_router(webhook_router)

# Настройка логгера
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}