"""
Пример бота с использованием Webhook.

Webhook - это метод получения обновлений через HTTP callback от сервера.
Сервер MAX сам отправляет события на ваш HTTPS эндпоинт.

Преимущества:
- Мгновенная доставка событий
- Меньше нагрузки на сервер (нет постоянных запросов)
- Лучше подходит для продакшена

Недостатки:
- Требуется публичный HTTPS сервер
- Нужен домен с SSL сертификатом
- Сложнее в настройке для локальной разработки

Требования:
- Публичный HTTPS URL (можно использовать ngrok для тестов)
- Порт 443 (или проксирование)
- SSL сертификат
"""

import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F
from aiomax.enums.update_type import UpdateTypeEnum

load_dotenv()
token = os.getenv("MaxToken", "YOUR_TOKEN_HERE")

# Секретный ключ для проверки подлинности webhook запросов
WEBHOOK_SECRET = os.getenv("WebhookSecret", "your_secret_key_here")

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
            text="👋 Привет! Я бот с Webhook.\n\n"
                 "Webhook обеспечивает мгновенную доставку событий!\n\n"
                 "Доступные команды:\n"
                 "/menu - Показать меню\n"
                 "/info - Информация о webhook"
        )


@bot.on_message(F.command("info"))
async def show_webhook_info(update):
    """Показ информации о webhook"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # Получаем текущие подписки
        try:
            subscriptions = await bot.get_subscriptions()
            info_text = f"📡 Информация о Webhook:\n\n"

            if subscriptions.subscriptions:
                for sub in subscriptions.subscriptions:
                    info_text += f"URL: {sub.url}\n"
                    info_text += f"Типы: {', '.join(sub.update_types)}\n\n"
            else:
                info_text += "Нет активных подписок\n"

            await bot.send_message(
                chat_id=chat_id,
                text=info_text
            )
        except Exception as e:
            await bot.send_message(
                chat_id=chat_id,
                text=f"❌ Ошибка получения информации: {e}"
            )


@bot.on_message(F.command("menu"))
async def show_menu(update):
    """Показ меню с inline кнопками"""
    if update.message and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id

        # ✅ Исправлено: ключ "buttons" внутри payload
        keyboard = {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "⚡ Быстрый ответ",
                        "payload": "fast_reply"
                    },
                    {
                        "type": "callback",
                        "text": "🔔 Уведомление",
                        "payload": "send_notification"
                    }
                ],
                [
                    {
                        "type": "link",
                        "text": "📚 Документация",
                        "url": "https://example.com/docs"
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


@bot.on_callback(F.callback.data("fast_reply"))
async def handle_fast_reply(update):
    """Быстрый ответ с обновлением сообщения"""
    if update.message and update.message.recipient.chat_id:
        # Используем answer_callback для ответа на callback
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            message={
                "text": "⚡ Это быстрый ответ через Webhook!\n\n"
                        "Webhook обеспечивает минимальную задержку.",
                "attachments": [{
                    "type": "inline_keyboard",
                    "payload": {
                        "buttons": [
                            [
                                {
                                    "type": "callback",
                                    "text": "🔄 Еще раз",
                                    "payload": "fast_reply"
                                },
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


@bot.on_callback(F.callback.data("send_notification"))
async def handle_notification(update):
    """Отправка одноразового уведомления"""
    if update.message and update.message.recipient.chat_id:
        # Отправляем только уведомление без изменения сообщения
        await bot.answer_callback(
            callback_id=update.callback.callback_id,
            notification="🔔 Это одноразовое уведомление!"
        )


@bot.on_callback(F.callback.contains("back"))
async def handle_back_callback(update):
    """Обработка кнопки назад"""
    await show_menu(update)


@bot.on_bot_started()
async def handle_bot_started(update):
    """Обработка запуска бота"""
    print(f"🤖 Бот был запущен пользователем ID: {update.user_id}")


# ============================================
# НАСТРОЙКА WEBHOOK
# ============================================

async def setup_webhook():
    """Настройка webhook подписки"""
    # Ваш публичный HTTPS URL
    # Для локальной разработки можно использовать ngrok:
    # ngrok http 8080
    webhook_url = os.getenv("WebhookUrl", "https://your-domain.com/webhook")

    print(f"📡 Настройка webhook: {webhook_url}")

    try:
        # Сначала удалим старые подписки если есть
        subscriptions = await bot.get_subscriptions()
        for sub in subscriptions.subscriptions:
            await bot.delete_subscription(url=sub.url)
            print(f"❌ Удалена старая подписка: {sub.url}")

        # Создаем новую подписку
        result = await bot.set_subscription(
            url=webhook_url,
            update_types=[
                "message_created",
                "message_callback",
                "bot_started"
            ],
            secret=WEBHOOK_SECRET
        )

        print(f"✅ Webhook настроен успешно!")
        return True

    except Exception as e:
        print(f"❌ Ошибка настройки webhook: {e}")
        return False


# ============================================
# ЗАПУСК БОТА
# ============================================

async def main():
    """Запуск бота через Webhook"""
    await bot.start()

    # Настраиваем webhook
    webhook_configured = await setup_webhook()

    if not webhook_configured:
        print("⚠️ Webhook не настроен. Запуск в режиме polling...")
        await bot.start_polling(
            types=[
                UpdateTypeEnum.MESSAGE_CREATED,
                UpdateTypeEnum.MESSAGE_CALLBACK,
                UpdateTypeEnum.BOT_STARTED
            ]
        )
        await bot.close()
        return

    print("\n🚀 Запуск webhook сервера...")
    print(f"📍 Endpoint: http://0.0.0.0:8080/webhook")
    print("💡 Для локальных тестов используйте: ngrok http 8080")
    print("Нажмите Ctrl+C для остановки\n")

    try:
        # Запускаем webhook сервер
        await bot.start_webhook(
            host="0.0.0.0",
            port=8080,
            path="/webhook",
            webhook_url=None,  # URL уже зарегистрирован в setup_webhook()
            secret=WEBHOOK_SECRET
        )

        # Держим сервер запущенным
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")

        # Очищаем webhook подписку
        try:
            webhook_url = os.getenv("WebhookUrl", "https://your-domain.com/webhook")
            await bot.delete_subscription(url=webhook_url)
            print(f"❌ Webhook подписка удалена")
        except Exception:
            pass

    finally:
        await bot.close()
        print("✅ Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())