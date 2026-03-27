import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F

load_dotenv()
token = os.getenv("MaxToken")

bot = Bot(token=token)

# ID администраторов и разрешенных чатов
ADMIN_IDS = [123456789]  # Замените на реальные ID
ALLOWED_CHAT_IDS = [-1001234567890]  # Замените на реальные ID чатов


@bot.on_message(F.user(*ADMIN_IDS))
async def admin_handler(update):
    """Обработчик только для администраторов"""
    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="👑 Привет, администратор!"
        )


@bot.on_message(F.chat(*ALLOWED_CHAT_IDS))
async def allowed_chat_handler(update):
    """Обработчик только для разрешенных чатов"""
    if update.message and update.message.body.text and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text=f"Сообщение из разрешенного чата: {update.message.body.text}"
        )


@bot.on_message(F.command("admin"))
async def admin_command(update):
    """Команда доступная только в определенных чатах"""
    if update.chat_id not in ALLOWED_CHAT_IDS:
        return

    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="Админ-панель доступна только в разрешенных чатах."
        )


# Комбинирование фильтров
@bot.on_message(F.user(*ADMIN_IDS) & F.text.contains("статус"))
async def admin_status_check(update):
    """Проверка статуса только для админов"""
    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="✅ Система работает нормально"
        )


async def main():
    await bot.start()
    print("Запуск бота с фильтрами...")
    await bot.start_polling()
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())