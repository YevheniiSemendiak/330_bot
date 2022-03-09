""" This is a 330 bot. """

import logging
import os

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = os.environ["BOT_TOKEN"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])  # type: ignore
async def send_welcome(message: types.Message) -> None:
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "Привіт! Я бот волонтерської організації 3/30. "
        "Поки працюю в ролі папуги, оскільки знаходжусь в розробці."
    )


@dp.message_handler(regexp="контакт|номер|number|contact")  # type: ignore
async def contacts(message: types.Message) -> None:
    await message.reply("Контактний номер уточнюється.")


@dp.message_handler()  # type: ignore
async def echo(message: types.Message) -> None:
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
