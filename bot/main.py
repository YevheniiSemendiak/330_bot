import logging

from aiogram import Dispatcher, executor
from aiogram.utils.executor import start_webhook

import bot.menu  # noqa: F401
from bot.bot import (
    API_TOKEN,
    HEROKU_APP_NAME,
    WEBAPP_HOST,
    WEBAPP_PORT,
    WEBHOOK_URL,
    bot_instance,
    dp,
)


logging.basicConfig(level=logging.INFO)


async def on_startup(dp: Dispatcher) -> None:
    await bot_instance.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp: Dispatcher) -> None:
    logging.warning("Shutting down..")

    # Remove webhook (not acceptable in some cases)
    await bot_instance.delete_webhook()

    logging.warning("Bye!")


if __name__ == "__main__":
    if HEROKU_APP_NAME:
        start_webhook(
            dispatcher=dp,
            webhook_path=f"/{API_TOKEN}",
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(
            dispatcher=dp,
            skip_updates=True,
        )
