from bot.core.common import safe_call
from bot.db.totp import (
    add_totp,
    get_totp
)
from bot.funcs.totp import (
    is_base32,
    totp_now,
    seconds_remaining
)
from pyrogram.enums import ChatType
from bot.config import logging_config
logging = logging_config.setup_logging(__name__)


async def start_command(_, message):
    text = (
        "/addtotp <BASE32> - set TOTP secret for group\n"
        "/getcode - get current 6-digit code"
    )

    if message.chat.type == ChatType.PRIVATE:
        text = "Add me to the group.\n" + text

    await safe_call(
        message.reply_text,
        text=text,
        quote=True
    )


async def add_totp_command(_, message):
    chat_id = message.chat.id
    text = message.text.split(maxsplit=1)
    if len(text) <= 1:
        await safe_call(
            message.reply_text,
            text="Specify the Base32 secret: /addtotp ABCDEF123...",
            quote=True
        )
        return
    base = text[1]
    if not is_base32(base):
        await safe_call(
            message.reply_text,
            text="It appears that this is not a Base32 secret. Please check and try again.",
            quote=True
        )
        return
    if await add_totp(chat_id, base):
        await safe_call(
            message.reply_text,
            text="The secret is saved for this chat.",
            quote=True
        )
    else:
        await safe_call(
            message.reply_text,
            text="Unable to keep the secret.",
            quote=True
        )


async def get_code_command(_, message):
    chat_id = message.chat.id
    base = await get_totp(chat_id)
    if not base:
        await safe_call(
            message.reply_text,
            text="The secret is not set. Use /addtotp <BASE32>.",
            quote=True
        )
        return
    try:
        code = totp_now(base, digits=6, interval=30)
        left = seconds_remaining(30)
        await safe_call(
            message.reply_text,
            text=f"Code: <code>{code}</code>\nWill change in: {left} sec",
            quote=True
        )
    except Exception as e:
        await safe_call(
            message.reply_text,
            text=f"Code generation error.",
            quote=True
        )
        logging.error(f"Code generation error {e}")


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

