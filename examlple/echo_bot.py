"""
Пример простого эхо-бота.

Демонстрирует базовое использование фильтров и обработчиков.
"""
import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F

load_dotenv()
token = os.getenv("MaxToken")

bot = Bot(token=token)


@bot.on_message(F.text.contains("привет"))
async def handle_hello(update):
    """Ответ на приветствие"""
    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="Привет! Как дела?"
        )


@bot.on_message(F.command("start"))
async def handle_start(update):
    """Обработка команды /start"""
    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="Добро пожаловать! Я эхо-бот."
        )


@bot.on_message()
async def echo_handler(update):
    """Эхо для всех остальных сообщений"""
    if update.message and update.message.body.text and update.message.recipient.chat_id:
        text = update.message.body.text
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text=f"Вы написали: {text}"
        )


async def main():
    await bot.start()
    print("Запуск эхо-бота...")
    await bot.start_polling()
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())