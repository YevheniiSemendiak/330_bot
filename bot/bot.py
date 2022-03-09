""" This is a 330 bot. """

import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook


API_TOKEN = os.environ["BOT_TOKEN"]
HEROKU_APP_NAME = os.environ["HEROKU_APP_NAME"]

# webhook settings
WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{API_TOKEN}"

# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ["PORT"])

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])  # type: ignore
async def send_welcome(message: types.Message) -> SendMessage:
    text = (
        "Привіт! Я бот волонтерської організації 3/30. "
        "Поки працюю в ролі папуги, оскільки знаходжусь в розробці."
    )
    return SendMessage(message.chat.id, text, reply_to_message_id=message.message_id)


@dp.message_handler(regexp="контакт|номер|number|contact")  # type: ignore
async def contacts(message: types.Message) -> SendMessage:
    return SendMessage(
        message.chat.id,
        "Контактний номер уточнюється.",
        reply_to_message_id=message.message_id,
    )


@dp.message_handler()  # type: ignore
async def echo(message: types.Message) -> SendMessage:
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp: Dispatcher) -> None:
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp: Dispatcher) -> None:
    logging.warning("Shutting down..")

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    logging.warning("Bye!")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=f"/{API_TOKEN}",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
