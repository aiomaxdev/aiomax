"""
Пример бота с callback кнопками.

Демонстрирует обработку callback данных от inline кнопок.
"""
import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F
from aiomax.enums.update_type import UpdateTypeEnum

load_dotenv()
token = os.getenv("MaxToken", "YOUR_TOKEN_HERE")

bot = Bot(token=token)


@bot.on_message(F.command("start"))
async def handle_start(update):
    """Обработка команды /start"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        await bot.send_message(
            chat_id=chat_id,
            text="👋 Привет! Я бот с callback кнопками.\n\n"
                 "Нажмите /menu чтобы показать меню с кнопками."
        )


@bot.on_message(F.command("menu"))
async def show_menu(update):
    """Показ меню с кнопками"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # ✅ Исправлено: ключ "buttons" внутри payload
        keyboard = {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "📊 Статистика",
                        "payload": "stats"
                    },
                    {
                        "type": "callback",
                        "text": "⚙️ Настройки",
                        "payload": "settings"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "ℹ️ О боте",
                        "payload": "about"
                    }
                ]
            ]
        }

        await bot.send_message(
            chat_id=chat_id,
            text="Выберите действие:",
            attachments=[{
                "type": "inline_keyboard",
                "payload": keyboard
            }]
        )


@bot.on_callback(F.callback.data("stats"))
async def handle_stats_callback(update):
    """Обработка callback статистики"""
    if update.message and update.message.recipient.chat_id:
        # ✅ Исправлено: используем answer_callback для ответа на callback
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "📊 Статистика:\n"
                        "• Пользователей: 100\n"
                        "• Сообщений обработано: 500\n"
                        "• Аптайм: 99.9%",
                "attachments": [{
                    "type": "inline_keyboard",
                    "payload": {
                        "buttons": [
                            [
                                {
                                    "type": "callback",
                                    "text": "🔙 Назад",
                                    "payload": "back_to_menu"
                                }
                            ]
                        ]
                    }
                }]
            }
        )


@bot.on_callback(F.callback.data("settings"))
async def handle_settings_callback(update):
    """Обработка callback настроек"""
    if update.message and update.message.recipient.chat_id:
        # ✅ Исправлено: используем answer_callback для ответа на callback
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "⚙️ Настройки:",
                "attachments": [{
                    "type": "inline_keyboard",
                    "payload": {
                        "buttons": [
                            [
                                {
                                    "type": "callback",
                                    "text": "🔔 Уведомления: ВКЛ",
                                    "payload": "toggle_notifications"
                                }
                            ],
                            [
                                {
                                    "type": "callback",
                                    "text": "🔙 Назад",
                                    "payload": "back_to_menu"
                                }
                            ]
                        ]
                    }
                }]
            }
        )


@bot.on_callback(F.callback.data("about"))
async def handle_about_callback(update):
    """Обработка callback о боте"""
    if update.message and update.message.recipient.chat_id:
        # ✅ Исправлено: используем answer_callback для ответа на callback
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "ℹ️ О боте:\n\n"
                        "Это пример бота с callback кнопками.\n"
                        "Фреймворк: aiomax\n"
                        "Версия: 1.0"
            }
        )


@bot.on_callback(F.callback.contains("back"))
async def handle_back_callback(update):
    """Обработка кнопки назад"""
    await show_menu(update)


async def main():
    await bot.start()
    print("🚀 Запуск callback бота...")
    print("Нажмите Ctrl+C для остановки")
    try:
        await bot.start_polling(
            limit=100,
            timeout=30,
            types=[
                UpdateTypeEnum.MESSAGE_CREATED,
                UpdateTypeEnum.MESSAGE_CALLBACK,
                UpdateTypeEnum.BOT_STARTED
            ]
        )
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
    finally:
        await bot.close()
        print("✅ Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())