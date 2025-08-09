import pyrogram.filters
import pyrogram.handlers.message_handler
from bot.funcs.base import (
    start_command,
    add_totp_command,
    get_code_command
)

def init_handlers(app):
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            start_command,
            pyrogram.filters.command("start")
        )
    )
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            add_totp_command,
            pyrogram.filters.command("addtotp") &
                pyrogram.filters.group
        )
    )
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            get_code_command,
            pyrogram.filters.command("getcode") &
                pyrogram.filters.group
        )
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

