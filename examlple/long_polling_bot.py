"""
Пример бота с использованием Long Polling.

Long Polling - это метод получения обновлений от сервера через постоянные запросы.
Бот сам запрашивает новые события у сервера с заданным интервалом.

Преимущества:
- Не требует публичного HTTPS сервера
- Простая настройка и запуск
- Хорошо подходит для разработки и тестирования

Недостатки:
- Большая задержка по сравнению с webhook
- Постоянные запросы к серверу
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


# ============================================
# ОБРАБОТЧИКИ СОБЫТИЙ
# ============================================

@bot.on_message(F.command("start"))
async def handle_start(update):
    """Обработка команды /start"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        await bot.send_message(
            chat_id=chat_id,
            text="👋 Привет! Я бот с Long Polling.\n\n"
                 "Доступные команды:\n"
                 "/menu - Показать меню с кнопками\n"
                 "/help - Помощь"
        )


@bot.on_message(F.command("menu"))
async def show_menu(update):
    """Показ меню с inline кнопками"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # ✅ Исправлено: ключ "buttons" внутри payload (а не "inline_keyboard")
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
                        "type": "link",
                        "text": "🌐 Наш сайт",
                        "url": "https://example.com"
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
    """Обработка callback кнопки статистики"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # ✅ Исправлено: "buttons" вместо "inline_keyboard" внутри payload
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "📊 Статистика бота:\n"
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
    """Обработка callback кнопки настроек"""
    if update.message and update.message.recipient.chat_id:
        # ✅ Исправлено: "buttons" вместо "inline_keyboard" внутри payload
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
    """Обработка callback кнопки о боте"""
    if update.message and update.message.recipient.chat_id:
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "ℹ️ О боте:\n\n"
                        "Это пример бота с использованием Long Polling.\n"
                        "Фреймворк: aiomax\n"
                        "Версия: 1.0\n\n"
                        "Long Polling позволяет получать обновления без настройки webhook."
            }
        )


@bot.on_callback(F.callback.contains("back"))
async def handle_back_callback(update):
    """Обработка кнопки назад"""
    await show_menu(update)


@bot.on_message()
async def echo_handler(update):
    """Эхо для всех текстовых сообщений"""
    if update.message and update.message.body.text and update.message.recipient.chat_id:
        text = update.message.body.text
        chat_id = update.message.recipient.chat_id

        await bot.send_message(
            chat_id=chat_id,
            text=f"💬 Вы написали: {text}"
        )


# ============================================
# ЗАПУСК БОТА
# ============================================

async def main():
    """Запуск бота через Long Polling"""
    await bot.start()

    print("🚀 Запуск бота через Long Polling...")
    print("Нажмите Ctrl+C для остановки")

    try:
        # Запускаем polling с указанием типов обновлений
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