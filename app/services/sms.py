"""
Fast2SMS OTP Service
"""
import httpx
import logging

logger = logging.getLogger(__name__)

FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"


async def send_otp_sms(phone: str, otp: str) -> bool:
    from app.core.config import settings
    api_key = getattr(settings, "FAST2SMS_API_KEY", None)
    if not api_key:
        logger.warning(f"Fast2SMS key not set. OTP for {phone}: {otp}")
        return False
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                FAST2SMS_URL,
                headers={"authorization": api_key},
                data={
                    "route": "otp",
                    "variables_values": otp,
                    "flash": 0,
                    "numbers": phone,
                },
            )
            result = response.json()
            if result.get("return") is True:
                logger.info(f"OTP sent successfully to {phone}")
                return True
            else:
                logger.error(f"Fast2SMS error: {result}")
                return False
    except Exception as e:
        logger.error(f"SMS send failed: {e}")
        return False
