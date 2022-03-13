import logging
import sys
from asyncio.exceptions import CancelledError

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
LOGGER = logging.getLogger(__name__)


async def on_startup(dp: Dispatcher) -> None:
    current_webhook = await bot_instance.get_webhook_info()
    if current_webhook.url == WEBHOOK_URL:
        LOGGER.info(f"The webhook is already registered.")
    elif not current_webhook.url:
        await bot_instance.set_webhook(WEBHOOK_URL)
    else:
        LOGGER.error(
            "Current webhook differs from the registered one: "
            f"{current_webhook} != {WEBHOOK_URL}"
        )


async def on_shutdown(dp: Dispatcher) -> None:
    LOGGER.warning("Shutting down..")

    exc_type, exc_inst, _ = sys.exc_info()
    if exc_type and isinstance(exc_inst, (CancelledError, KeyboardInterrupt)):
        LOGGER.warning(
            f"Keeping webhook to continue routing traffic. Interrupted with {exc_type}."
        )
    else:
        LOGGER.error(f"Removing webhook since got unexpected {exc_type}: {exc_inst}")
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
