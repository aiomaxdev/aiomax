"""
Пример использования обновленного фреймворка aiomax с диспетчеризацией событий

Этот файл демонстрирует новые возможности:
- Декораторы для регистрации обработчиков (@bot.on_message, @bot.on_bot_started, и т.д.)
- Автоматическая диспетчеризация обновлений при polling
- Поддержка Webhook с встроенным сервером
- Методы для управления подписками на Webhook
"""

import asyncio
import os
from dotenv import load_dotenv
from aiomax import Bot, UpdateTypeEnum

load_dotenv()
token = os.getenv("MaxToken")

bot = Bot(token=token)


# ============================================
# ПРИМЕР 1: Использование декораторов для обработки событий
# ============================================

@bot.on_message
async def handle_message(update):
    """Обработчик новых сообщений"""
    if update.message and update.message.body.text:
        text = update.message.body.text
        print(f"Получено сообщение: {text}")

        # Эхо-ответ
        if update.message.recipient.chat_id:
            await bot.send_message(
                chat_id=update.message.recipient.chat_id,
                text=f"Вы написали: {text}"
            )


@bot.on_bot_started
async def handle_bot_started(update):
    """Обработчик запуска бота"""
    print(f"Бот был запущен пользователем {update.user_id}")


@bot.on_callback
async def handle_callback(update):
    """Обработчик callback от кнопок"""
    print(f"Получен callback: {update}")


@bot.on_message_edited
async def handle_message_edited(update):
    """Обработчик редактирования сообщения"""
    print(f"Сообщение было отредактировано: {update}")


@bot.on_message_removed
async def handle_message_removed(update):
    """Обработчик удаления сообщения"""
    print(f"Сообщение было удалено: {update}")


# ============================================
# ПРИМЕР 2: Запуск polling с автоматической диспетчеризацией
# ============================================

async def run_polling_example():
    """Запуск бота через long polling"""
    await bot.start()

    print("Запуск polling...")

    # Polling теперь автоматически диспетчеризирует обновления
    # и вызывает зарегистрированные обработчики
    await bot.start_polling(
        limit=100,
        timeout=30,
        types=[
            UpdateTypeEnum.MESSAGE_CREATED,
            UpdateTypeEnum.BOT_STARTED,
            UpdateTypeEnum.MESSAGE_CALLBACK
        ]
    )

    await bot.close()


# ============================================
# ПРИМЕР 3: Использование Webhook
# ============================================

async def run_webhook_example():
    """Запуск бота через Webhook"""
    await bot.start()

    # Настройка и запуск webhook сервера
    # Важно: ваш сервер должен быть доступен по HTTPS на порту 443
    await bot.start_webhook(
        host="0.0.0.0",
        port=8080,
        path="/webhook",
        secret="your_secret_key"  # секрет для проверки подлинности запросов
    )

    # Держим сервер запущенным
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await bot.close()


# ============================================
# ПРИМЕР 4: Управление подписками на Webhook
# ============================================

async def manage_subscriptions_example():
    """Пример управления подписками на Webhook"""
    await bot.start()

    # Получить текущие подписки
    subscriptions = await bot.get_subscriptions()
    print(f"Текущие подписки: {subscriptions}")

    # Создать новую подписку
    result = await bot.set_subscription(
        url="https://your-domain.com/webhook",
        update_types=["message_created", "bot_started"],
        secret="your_secret_key"
    )
    print(f"Результат создания подписки: {result}")

    # Удалить подписку
    result = await bot.delete_subscription(url="https://your-domain.com/webhook")
    print(f"Результат удаления подписки: {result}")

    await bot.close()


# ============================================
# ПРИМЕР 5: Ручная регистрация обработчиков
# ============================================

async def manual_handler_registration_example():
    """Пример ручной регистрации обработчиков"""
    await bot.start()

    async def custom_handler(update):
        print(f"Кастомный обработчик: {update}")

    # Регистрация обработчика для конкретного типа события
    bot.register_handler(UpdateTypeEnum.USER_ADDED, custom_handler)

    # Или можно использовать строку вместо enum
    bot.register_handler("user_removed", custom_handler)

    await bot.start_polling()
    await bot.close()


# ============================================
# ЗАПУСК
# ============================================

async def main():
    # Раскомментируйте нужный пример

    # Пример 1: Polling с декораторами
    await run_polling_example()

    # Пример 2: Webhook
    # await run_webhook_example()

    # Пример 3: Управление подписками
    # await manage_subscriptions_example()

    # Пример 4: Ручная регистрация обработчиков
    # await manual_handler_registration_example()


if __name__ == "__main__":
    asyncio.run(main())