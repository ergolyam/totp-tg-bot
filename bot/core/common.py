import asyncio
from typing import cast
from pyrogram.errors import FloodWait
from bot.config import logging_config
logging = logging_config.setup_logging(__name__)


async def safe_call(func, *args, **kwargs):
    for _ in range(5):
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            wait_sec: int = cast(int, e.value)
            await asyncio.sleep(wait_sec + 1)
    raise


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

