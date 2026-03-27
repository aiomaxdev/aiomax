"""
Пример бота с callback кнопками.

Демонстрирует обработку callback данных от inline кнопок.
"""
import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F

load_dotenv()
token = os.getenv("MaxToken")

bot = Bot(token=token)


@bot.on_message(F.command("menu"))
async def show_menu(update):
    """Показ меню с кнопками"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # Создаем inline клавиатуру
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "📊 Статистика", "callback_data": "stats"},
                    {"text": "⚙️ Настройки", "callback_data": "settings"}
                ],
                [
                    {"text": "ℹ️ О боте", "callback_data": "about"}
                ]
            ]
        }

        await bot.send_message(
            chat_id=chat_id,
            text="Выберите действие:",
            attachments=[{"type": "keyboard", "payload": keyboard}]
        )


@bot.on_callback(F.callback.data("stats"))
async def handle_stats_callback(update):
    """Обработка callback статистики"""
    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="📊 Статистика:\n- Пользователей: 100\n- Сообщений: 500"
        )


@bot.on_callback(F.callback.data("settings"))
async def handle_settings_callback(update):
    """Обработка callback настроек"""
    if update.message and update.message.recipient.chat_id:
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🔔 Уведомления: ВКЛ", "callback_data": "toggle_notifications"},
                ],
                [
                    {"text": "🔙 Назад", "callback_data": "back_to_menu"}
                ]
            ]
        }

        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="⚙️ Настройки:",
            attachments=[{"type": "keyboard", "payload": keyboard}]
        )


@bot.on_callback(F.callback.data("about"))
async def handle_about_callback(update):
    """Обработка callback о боте"""
    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="ℹ️ О боте:\nЭто пример бота с callback кнопками.\nВерсия: 1.0"
        )


@bot.on_callback(F.callback.contains("back"))
async def handle_back_callback(update):
    """Обработка кнопки назад"""
    if update.message and update.message.recipient.chat_id:
        await show_menu(update)


async def main():
    await bot.start()
    print("Запуск callback бота...")
    await bot.start_polling(types=["message_created", "message_callback"])
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())