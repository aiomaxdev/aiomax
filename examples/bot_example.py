"""
Пример использования Dispatcher в стиле aiogram.

Этот пример демонстрирует:
1. Создание роутеров для группировки хендлеров
2. Использование фильтров F
3. Работу с FSM (конечный автомат)
4. Middleware для логирования
5. Иерархию роутеров
"""

import asyncio
from aiomax import Bot, Router, Dispatcher, F, State, StatesGroup, MemoryStorage
from aiomax.handlers.middleware import LoggingMiddleware


# 1. Создаём группу состояний для FSM
class MyStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()


# 2. Создаём основной роутер
main_router = Router(name="main")


# 3. Регистрируем обработчик команды /start
@main_router.on_message(F.Command("/start"))
async def start_handler(event: dict, context: dict):
    """Обработчик команды /start"""
    bot = context["bot"]
    fsm = context["fsm"]
    
    # Устанавливаем состояние ожидания имени
    await fsm.set_state(MyStates.waiting_for_name)
    
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text="Привет! Я бот. Как тебя зовут?"
    )


# 4. Обработчик имени (срабатывает только в состоянии waiting_for_name)
@main_router.on_message(F.State(MyStates.waiting_for_name))
async def get_name_handler(event: dict, context: dict):
    """Получаем имя пользователя"""
    bot = context["bot"]
    fsm = context["fsm"]
    
    name = event["message"]["body"]["text"]
    
    # Сохраняем имя в данные FSM
    await fsm.update_data({"name": name})
    await fsm.set_state(MyStates.waiting_for_age)
    
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text=f"Приятно познакомиться, {name}! Сколько тебе лет?"
    )


# 5. Обработчик возраста
@main_router.on_message(F.State(MyStates.waiting_for_age))
async def get_age_handler(event: dict, context: dict):
    """Получаем возраст и завершаем регистрацию"""
    bot = context["bot"]
    fsm = context["fsm"]
    
    age = event["message"]["body"]["text"]
    data = await fsm.get_data()
    name = data.get("name", "друг")
    
    # Сбрасываем состояние
    await fsm.reset_state()
    await fsm.set_data({})
    
    chat_id = event["message"]["recipient"]["chat_id"]
    await bot.send_message(
        chat_id=chat_id,
        text=f"Отлично, {name}! Тебе {age} лет. Регистрация завершена!"
    )


# 6. Обработчик текста "привет" (фильтр по содержимому)
@main_router.on_message(F.Text(contains="привет"))
async def hello_handler(event: dict, context: dict):
    """Ответ на приветствие"""
    bot = context["bot"]
    chat_id = event["message"]["recipient"]["chat_id"]
    
    await bot.send_message(
        chat_id=chat_id,
        text="Привет! Напиши /start чтобы начать."
    )


# 7. Создаём дополнительный роутер для админских команд
admin_router = Router(name="admin")


@admin_router.on_message(F.Command("/admin"))
async def admin_handler(event: dict, context: dict):
    """Админская команда"""
    bot = context["bot"]
    chat_id = event["message"]["recipient"]["chat_id"]
    
    # Проверка прав (можно добавить фильтр)
    await bot.send_message(
        chat_id=chat_id,
        text="Это админская панель."
    )


async def main():
    # Токен бота (замените на свой)
    TOKEN = "YOUR_TOKEN_HERE"
    
    # Создаём бота
    bot = Bot(TOKEN)
    
    # Создаём диспетчер с хранилищем состояний
    dp = Dispatcher(storage=MemoryStorage())
    
    # Добавляем middleware для логирования
    dp.add_middleware(LoggingMiddleware())
    
    # Подключаем роутеры к диспетчеру
    dp.include_router(main_router)
    dp.include_router(admin_router)
    
    # Запускаем бота
    await bot.start()
    
    print("Бот запущен...")
    
    try:
        # Запускаем polling
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Остановка бота...")
    finally:
        await bot.close()


if __name__ == "__main__":
    # asyncio.run(main())
    print("Пример готов к запуску!")
    print("Замените TOKEN на ваш токен и раскомментируйте asyncio.run(main())")
