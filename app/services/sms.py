"""
Fast2SMS OTP Service (Quick SMS route - no DLT registration required)
"""
import httpx
import logging

logger = logging.getLogger(__name__)

FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"


async def send_otp_sms(phone: str, otp: str) -> bool:
    from app.core.config import settings

    api_key = getattr(settings, "FAST2SMS_API_KEY", None)
    if not api_key:
        logger.warning(f"[FALLBACK] Fast2SMS key not set. OTP for {phone}: {otp}")
        return True
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                FAST2SMS_URL,
                params={
                    "authorization": api_key,
                    "message": f"Your PrintLab OTP is {otp}. Do not share this with anyone.",
                    "language": "english",
                    "route": "q",
                    "numbers": phone,
                },
            )
            result = response.json()
            if result.get("return") is True:
                logger.info(f"OTP sent successfully to {phone}")
                return True
            else:
                logger.error(f"Fast2SMS error: {result}")
                logger.warning(f"[FALLBACK] Real SMS failed. OTP for {phone}: {otp}")
                return True
    except Exception as e:
        logger.error(f"SMS send failed: {e}")
        logger.warning(f"[FALLBACK] Real SMS failed. OTP for {phone}: {otp}")
        return True
