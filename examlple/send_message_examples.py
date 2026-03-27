"""
Примеры использования различных методов отправки сообщений.

Демонстрирует различные способы использования send_message и answer_callback:
- Отправка текста
- Отправка с кнопками (inline keyboard)
- Форматирование текста (Markdown/HTML)
- Ответы на callback
- Одноразовые уведомления
"""

import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F

load_dotenv()
token = os.getenv("MaxToken", "YOUR_TOKEN_HERE")

bot = Bot(token=token)


# ============================================
# ПРИМЕР 1: Простая отправка текста
# ============================================

@bot.on_message(F.command("text"))
async def send_text_example(update):
    """Пример отправки простого текстового сообщения"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        await bot.send_message(
            chat_id=chat_id,
            text="Это простое текстовое сообщение"
        )


# ============================================
# ПРИМЕР 2: Отправка с кнопками
# ============================================

@bot.on_message(F.command("buttons"))
async def send_buttons_example(update):
    """Пример отправки сообщения с inline кнопками"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # Создаем клавиатуру с разными типами кнопок
        keyboard = {
            "buttons": [
                # Ряд с callback кнопками
                [
                    {
                        "type": "callback",
                        "text": "🔵 Callback 1",
                        "payload": "btn_1"
                    },
                    {
                        "type": "callback",
                        "text": "🔵 Callback 2",
                        "payload": "btn_2"
                    }
                ],
                # Ряд с link кнопкой
                [
                    {
                        "type": "link",
                        "text": "🌐 Открыть сайт",
                        "url": "https://example.com"
                    }
                ],
                # Ряд с одной кнопкой
                [
                    {
                        "type": "callback",
                        "text": "ℹ️ Информация",
                        "payload": "info"
                    }
                ]
            ]
        }

        await bot.send_message(
            chat_id=chat_id,
            text="Выберите кнопку:",
            attachments=[{
                "type": "inline_keyboard",
                "payload": keyboard
            }]
        )


# ============================================
# ПРИМЕР 3: Форматирование текста
# ============================================

@bot.on_message(F.command("format"))
async def send_formatted_example(update):
    """Пример отправки сообщения с форматированием"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # Markdown форматирование
        markdown_text = """
*Жирный текст*
_Курсив_
~Зачеркнутый~
`Моноширинный`

[Ссылка](https://example.com)
        """.strip()

        await bot.send_message(
            chat_id=chat_id,
            text=markdown_text,
            format="markdown"  # или "html"
        )


# ============================================
# ПРИМЕР 4: Отправка пользователю по user_id
# ============================================

@bot.on_message(F.command("send_user"))
async def send_to_user_example(update):
    """Пример отправки сообщения пользователю по user_id"""
    if update.message and update.message.recipient.chat_id:
        # В реальном боте здесь был бы конкретный user_id
        # Например, из базы данных
        target_user_id = 123456789  # Замените на реальный ID

        try:
            await bot.send_message(
                user_id=target_user_id,
                text="Сообщение отправлено по user_id"
            )
        except Exception as e:
            await bot.send_message(
                chat_id=update.message.recipient.chat_id,
                text=f"Ошибка: {e}"
            )


# ============================================
# ПРИМЕР 5: Отключение превью ссылок
# ============================================

@bot.on_message(F.command("nolinkpreview"))
async def disable_link_preview_example(update):
    """Пример отправки сообщения без превью ссылок"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        await bot.send_message(
            chat_id=chat_id,
            text="Проверьте ссылку: https://example.com",
            disable_link_preview=True  # Отключаем генерацию превью
        )


# ============================================
# ПРИМЕР 6: Ответ на callback с обновлением сообщения
# ============================================

@bot.on_callback(F.callback.data("btn_1"))
async def handle_btn1_callback(update):
    """Обработка callback с обновлением сообщения"""
    if update.message and update.message.recipient.chat_id:
        # Обновляем исходное сообщение
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "✅ Вы нажали кнопку 1!\n\n"
                        "Исходное сообщение обновлено.",
                "attachments": [{
                    "type": "inline_keyboard",
                    "payload": {
                        "buttons": [
                            [
                                {
                                    "type": "callback",
                                    "text": "🔙 Назад",
                                    "payload": "back"
                                }
                            ]
                        ]
                    }
                }]
            }
        )


@bot.on_callback(F.callback.data("btn_2"))
async def handle_btn2_callback(update):
    """Обработка callback с уведомлением"""
    if update.message and update.message.recipient.chat_id:
        # Отправляем только уведомление, не меняя сообщение
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            notification="🔔 Вы нажали кнопку 2!"
        )


@bot.on_callback(F.callback.data("info"))
async def handle_info_callback(update):
    """Обработка callback с информацией"""
    if update.message and update.message.recipient.chat_id:
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "ℹ️ Информация:\n\n"
                        "answer_callback позволяет:\n"
                        "1. Обновить исходное сообщение\n"
                        "2. Отправить одноразовое уведомление\n"
                        "3. Сделать и то, и другое одновременно"
            }
        )


@bot.on_callback(F.callback.contains("back"))
async def handle_back_callback(update):
    """Кнопка назад"""
    await send_buttons_example(update)


# ============================================
# ПРИМЕР 7: Отправка без уведомления участников
# ============================================

@bot.on_message(F.command("silent"))
async def send_silent_example(update):
    """Пример отправки сообщения без уведомления"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        await bot.send_message(
            chat_id=chat_id,
            text="🤫 Тихое сообщение (без звука уведомления)",
            notify=False  # Участники не получат уведомление
        )


# ============================================
# ПРИМЕР 8: Комбинированный ответ
# ============================================

@bot.on_message(F.command("combo"))
async def combo_example(update):
    """Пример комбинированного ответа"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        keyboard = {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "✏️ Редактировать",
                        "payload": "edit_message"
                    },
                    {
                        "type": "callback",
                        "text": "🔔 Уведомить",
                        "payload": "notify_only"
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


@bot.on_callback(F.callback.data("edit_message"))
async def handle_edit_callback(update):
    """Редактирование сообщения через callback"""
    await bot.answer_callback(
        callback_id=update.callback.callback_id,
        message={
            "text": "✏️ Сообщение отредактировано!\n\n"
                    "Теперь здесь новый текст.",
            "attachments": [{
                "type": "inline_keyboard",
                "payload": {
                    "buttons": [
                        [
                            {
                                "type": "callback",
                                "text": "🔙 Назад",
                                "payload": "back"
                            }
                        ]
                    ]
                }
            }]
        }
    )


@bot.on_callback(F.callback.data("notify_only"))
async def handle_notify_callback(update):
    """Только уведомление"""
    await bot.answer_callback(
        callback_id=update.callback.callback_id,
        notification="📬 Это только уведомление!"
    )


# ============================================
# СПРАВКА
# ============================================

@bot.on_message(F.command("help"))
async def show_help(update):
    """Показ справки по всем командам"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        help_text = """
📚 Справка по командам:

/text - Простое текстовое сообщение
/buttons - Сообщение с кнопками
/format - Форматирование текста (Markdown)
/send_user - Отправка по user_id
/nolinkpreview - Без превью ссылок
/silent - Тихое сообщение (без уведомления)
/combo - Комбинированный пример

Нажмите /buttons чтобы попробовать кнопки!
        """.strip()

        await bot.send_message(
            chat_id=chat_id,
            text=help_text,
            format="markdown"
        )


# ============================================
# ЗАПУСК
# ============================================

async def main():
    await bot.start()

    print("🚀 Запуск бота с примерами использования...")
    print("Доступные команды: /start, /help, /text, /buttons, /format, etc.")

    try:
        await bot.start_polling(
            types=["message_created", "message_callback"]
        )
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())