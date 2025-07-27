import hmac
import hashlib
from fastapi import HTTPException, status
from .config import settings


def verify_signature(body: bytes, signature: str) -> bool:
    """
    Проверяет HMAC-SHA1 подпись от Pyrus.
    Использует SECRET_KEY из .env
    """
    digest = hmac.new(
        key=settings.secret_key.encode(),
        msg=body,
        digestmod=hashlib.sha1
    ).hexdigest()
    return hmac.compare_digest(digest, signature.lower())


async def validate_webhook_signature(request):
    signature = request.headers.get("X-Pyrus-Sig")
    if not signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature header"
        )

    if not verify_signature(await request.body(), signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )