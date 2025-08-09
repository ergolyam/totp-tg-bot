from typing import Optional
from tortoise.transactions import in_transaction
from bot.db.models import Totp


async def add_totp(chat_id: int, key: str) -> bool:
    try:
        async with in_transaction():
            obj = await Totp.get_or_none(chat_id=chat_id)
            if obj is None:
                await Totp.create(chat_id=chat_id, totp_key=key)
            else:
                obj.totp_key = key
                await obj.save()
        return True
    except Exception:
        return False


async def get_totp(chat_id: int) -> str:
    obj: Optional[Totp] = await Totp.get_or_none(chat_id=chat_id)
    if obj is None:
        return ""
    return obj.totp_key


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

