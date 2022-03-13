""" This is a 330 bot. """

import os

from aiogram import Bot, Dispatcher


API_TOKEN = os.environ["BOT_TOKEN"]
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")

# webhook settings
WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{API_TOKEN}"

# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", "8080"))


# Initialize bot and dispatcher
bot_instance = Bot(token=API_TOKEN)
dp = Dispatcher(bot_instance)
