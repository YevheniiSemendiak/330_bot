from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from .bot import dp


@dp.message_handler(commands=["start", "help"])  # type: ignore
async def send_welcome(message: types.Message, text: str = "") -> SendMessage:
    text = text or (
        "Привіт! Я бот волонтерської організації 3/30. "
        "Поки працюю в ролі папуги, оскільки знаходжусь в розробці."
    )
    keyboard_markup = types.InlineKeyboardMarkup()
    text_and_data = (
        ("Меню", "menu"),
        ("Довідка", "help"),
    )
    row_btns = (
        types.InlineKeyboardButton(text, callback_data=data)
        for text, data in text_and_data
    )
    keyboard_markup.add(*row_btns)

    return SendMessage(
        message.chat.id,
        text,
        reply_to_message_id=message.message_id,
        reply_markup=keyboard_markup,
    )


@dp.callback_query_handler(text="menu")  # type: ignore
@dp.callback_query_handler(text="help")  # type: ignore
async def main_menu_callback_handler(query: types.CallbackQuery):  # type: ignore
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f"You answered with {answer_data!r}")

    if answer_data == "menu":
        return await main_menu_responce(query.message)
    elif answer_data == "help":
        return SendMessage(
            query.message.chat.id,
            "Бот в розробці. Долучайтеся до нашого каналу https://t.me/dobrobat330",
            reply_to_message_id=query.message.message_id,
        )
    else:
        return await send_welcome(
            query.message,
            "Вибачте, відповідь не зрозуміла.",
        )


@dp.message_handler(commands="menu")  # type: ignore
async def main_menu_responce(message: types.Message) -> SendMessage:
    keyboard_markup = types.InlineKeyboardMarkup()
    text_and_data = (
        ("Надаю допомогу", "provide_help"),
        ("Потребую допомоги", "need_help"),
    )
    row_btns = (
        types.InlineKeyboardButton(text, callback_data=data)
        for text, data in text_and_data
    )
    keyboard_markup.add(*row_btns)

    return SendMessage(
        chat_id=message.chat.id,
        text="Ви в головному меню.",
        reply_to_message_id=message.message_id,
        reply_markup=keyboard_markup,
    )


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
