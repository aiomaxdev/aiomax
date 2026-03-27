import asyncio
import os
import logging
from dotenv import load_dotenv
from aiohttp import web
from aiomax import Bot, Dispatcher, Router, F, MemoryStorage, LoggingMiddleware
from aiomax.enums.update_type import UpdateTypeEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Конфигурация
BOT_TOKEN = os.getenv("MaxToken")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)  # https://your-domain.com/webhook для production
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_super_secret_key")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Создаем роутер для группировки обработчиков
router = Router(name="main")


# ==================== ОБРАБОТЧИКИ КОМАНД ====================

@router.on_message(F.Command("/start"))
async def cmd_start(event, context):
    """Обработчик команды /start"""
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text="👋 Привет! Я бот на MAX Platform.\n\n"
             "Доступные команды:\n"
             "/start - Запустить бота\n"
             "/help - Помощь\n"
             "/ping - Проверка связи"
    )
    logger.info(f"Команда /start выполнена для чата {chat_id}")


@router.on_message(F.Command("/help"))
async def cmd_help(event, context):
    """Обработчик команды /help"""
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text="ℹ️ **Помощь**\n\n"
             "Этот бот демонстрирует работу с MAX Platform API.\n\n"
             "**Возможности:**\n"
             "- Обработка команд\n"
             "- Фильтрация сообщений\n"
             "- FSM (машина состояний)\n"
             "- Middleware\n"
             "- Webhook и Polling режимы"
    )


@router.on_message(F.Command("/ping"))
async def cmd_ping(event, context):
    """Обработчик команды /ping"""
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text="🟢 Pong! Бот работает."
    )


# ==================== ОБРАБОТЧИКИ СООБЩЕНИЙ ====================

@router.on_message(F.Text("привет"))
async def handle_hello(event, context):
    """Обработчик сообщения 'привет'"""
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text="👋 Привет! Как дела?"
    )


@router.on_message(F.Text("как дела?"))
async def handle_how_are_you(event, context):
    """Обработчик сообщения 'как дела?'"""
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text="✅ У меня всё отлично! Спасибо, что спросили 😊"
    )


# ==================== ОБРАБОТЧИК ВСЕХ СООБЩЕНИЙ (fallback) ====================

@router.on_message()
async def handle_all_messages(event, context):
    """Обработчик всех остальных сообщений"""
    chat_id = event["message"]["recipient"]["chat_id"]
    text = event["message"]["body"].get("text", "")
    
    # Отвечаем только если это не команда
    if not text.startswith("/"):
        await bot.send_message(
            chat_id=chat_id,
            text=f"📨 Получено сообщение: {text[:100]}"
        )


# Подключаем роутер к диспетчеру
dp.include_router(router)

# Добавляем middleware для логирования
dp.add_middleware(LoggingMiddleware())


async def start_webhook_app():
    """Запуск бота в режиме Webhook"""
    app = web.Application()
    
    async def webhook_handler(request):
        """Обработчик входящих webhook-запросов"""
        # Проверка секретного ключа
        secret = request.headers.get("X-Max-Bot-Api-Secret")
        if secret != WEBHOOK_SECRET:
            logger.warning("Неверный секретный ключ в webhook запросе")
            return web.Response(status=403, text="Forbidden")
        
        try:
            update = await request.json()
            logger.info(f"Получен webhook: {update.get('type', 'unknown')}")
            
            # Передаем обновление в диспетчер
            await dp.feed_update(bot, update)
            
            return web.Response(status=200, text="OK")
        except Exception as e:
            logger.error(f"Ошибка обработки webhook: {e}")
            return web.Response(status=500, text="Internal Server Error")
    
    app.router.add_post("/webhook", webhook_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    
    logger.info(f"Webhook сервер запущен на http://{HOST}:{PORT}/webhook")
    logger.info(f"Для настройки webhook выполните:")
    logger.info(f"curl -X POST 'https://platform-api.max.ru/subscriptions' \\")
    logger.info(f"  -H 'Authorization: {BOT_TOKEN}' \\")
    logger.info(f"  -H 'Content-Type: application/json' \\")
    logger.info(f"  -d '{{\"url\": \"https://your-domain.com/webhook\", \"secret\": \"{WEBHOOK_SECRET}\"}}'")
    
    return runner


async def start_polling_mode():
    """Запуск бота в режиме Polling"""
    logger.info("Запуск бота в режиме Polling...")
    
    await dp.start_polling(
        bot,
        limit=100,
        timeout=30,
        types=[UpdateTypeEnum.MESSAGE_CREATED, UpdateTypeEnum.MESSAGE_REMOVED]
    )


async def main():
    await bot.start()
    
    try:
        if WEBHOOK_URL:
            # Режим Webhook
            logger.info("Запуск в режиме Webhook...")
            runner = await start_webhook_app()
            
            # Держим сервер запущенным
            while True:
                await asyncio.sleep(3600)
        else:
            # Режим Polling
            await start_polling_mode()
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
