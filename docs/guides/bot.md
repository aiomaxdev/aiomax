# Bot

Класс `Bot` — это основной интерфейс для взаимодействия с API MAX мессенджера. Он предоставляет удобный высокоуровневый доступ ко всем методам API и управляет диспетчеризацией событий.

## Создание бота

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")
```

## Жизненный цикл

### Запуск

Перед использованием бота необходимо вызвать метод `start()`:

```python
await bot.start()
```

Это инициализирует HTTP-клиент для работы с API.

### Остановка

Для корректного завершения работы используйте метод `close()`:

```python
await bot.close()
```

Этот метод:
- Останавливает polling (если запущен)
- Останавливает webhook сервер (если запущен)
- Закрывает HTTP-сессию

## Основные методы API

### Информация о боте

```python
# Получить информацию о текущем боте
bot_info = await bot.get_me()
print(f"Username: {bot_info.username}")
```

### Работа с чатами

```python
# Получить список чатов
chats = await bot.get_chats()

# Получить информацию о конкретном чате
chat = await bot.get_chat_info_by_chat_id(chat_id=-123456)

# Изменить информацию о чате
await bot.patch_chat_info_by_chat_id(
    chat_id=-123456,
    title="Новое название"
)

# Удалить чат
await bot.delete_chat_by_chat_id(chat_id=-123456)
```

### Отправка сообщений

```python
# Отправить текстовое сообщение
response = await bot.send_message(
    chat_id=-123456,
    text="Привет, мир!"
)

# Отправить действие (typing, etc.)
await bot.send_action(
    chat_id=-123456,
    action="typing"
)
```

### Работа с сообщениями

```python
# Получить сообщение
message = await bot.get_message(
    chat_id=-123456,
    message_id=123
)

# Получить несколько сообщений
messages = await bot.get_messages(
    chat_id=-123456,
    limit=50
)

# Редактировать сообщение
await bot.edit_message(
    chat_id=-123456,
    message_id=123,
    text="Обновлённый текст"
)

# Удалить сообщение
await bot.delete_message(
    chat_id=-123456,
    message_id=123
)
```

### Закреплённые сообщения

```python
# Закрепить сообщение
await bot.pin_message(
    chat_id=-123456,
    message_id=123
)

# Открепить сообщение
await bot.unpin_message(chat_id=-123456)

# Получить закреплённое сообщение
pinned = await bot.get_pinned_message(chat_id=-123456)
```

### Участники чата

```python
# Получить участников чата
members = await bot.get_members_from_chat(chat_id=-123456)

# Добавить участника
await bot.add_members_to_chat(
    chat_id=-123456,
    user_ids=[123, 456]
)

# Удалить участника
await bot.delete_members_from_chat(
    chat_id=-123456,
    user_id=789
)
```

### Администраторы

```python
# Получить администраторов чата
admins = await bot.get_admins_from_chat(chat_id=-123456)

# Назначить администратора
await bot.add_admins_to_chat(
    chat_id=-123456,
    user_id=123,
    permissions=["can_delete_messages", "can_pin_messages"]
)

# Снять права администратора
await bot.delete_permissions_from_chat(
    chat_id=-123456,
    user_id=123
)
```

### Callback кнопки

```python
# Ответ на callback кнопки
await bot.answer_callback(
    callback_id="callback_123",
    message={
        "text": "Новое сообщение",
        "keyboard": {...}
    },
    notification="Уведомление"
)
```

## Получение обновлений

### Long Polling

```python
async def main():
    await bot.start()

    # Запуск polling с параметрами
    await bot.start_polling(
        limit=100,      # Максимум обновлений за запрос
        timeout=30,     # Таймаут long polling
        types=["message", "callback"]  # Фильтр по типам
    )

    await bot.close()
```

### Webhook

```python
async def main():
    await bot.start()

    # Запуск webhook сервера
    await bot.start_webhook(
        host="0.0.0.0",
        port=8080,
        path="/webhook",
        webhook_url="https://your-domain.com/webhook",
        secret="your-secret-key"
    )

    # Держим сервер запущенным
    import asyncio
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

    await bot.close()
```

## Обработчики событий

### Декораторы

```python
from aiomax import F

@bot.on_message()
async def handle_message(update):
    print(f"Получено сообщение: {update.message.body.text}")

@bot.on_callback()
async def handle_callback(update):
    print(f"Получен callback: {update.callback.data}")

@bot.on_bot_started()
async def on_start(update):
    print("Бот запущен!")

@bot.on_message_edited()
async def on_edit(update):
    print("Сообщение отредактировано")

@bot.on_message_removed()
async def on_remove(update):
    print("Сообщение удалено")
```

### С фильтрами

```python
@bot.on_message(F.text.contains("привет"))
async def handle_hello(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Привет! Как дела?"
    )

@bot.on_message(F.command("start"))
async def cmd_start(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Добро пожаловать!"
    )

@bot.on_callback(F.callback.data("buy"))
async def handle_buy(update):
    await bot.answer_callback(
        callback_id=update.callback.id,
        notification="Покупка оформлена"
    )
```

### Ручная регистрация

```python
from aiomax.enums.update_type import UpdateTypeEnum

async def my_handler(update):
    print(f"Update: {update}")

bot.register_handler(UpdateTypeEnum.MESSAGE_CREATED, my_handler)
```

## Middleware

Middleware позволяет обрабатывать обновления до и после вызова обработчиков:

```python
from aiomax.middleware.base import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def pre_process(self, update):
        print(f"Получено обновление: {update.update_id}")

    async def post_process(self, update, exception=None):
        if exception:
            print(f"Ошибка: {exception}")

bot.use_middleware(LoggingMiddleware())
```

## Пример полного бота

```python
import asyncio
from aiomax import Bot, F, StatesGroup, MemoryStorage, FSMManager

bot = Bot(token="YOUR_TOKEN")
fsm = FSMManager(MemoryStorage())

class FormState(StatesGroup):
    waiting_for_name = "waiting_for_name"
    waiting_for_age = "waiting_for_age"

@bot.on_message(F.command("start"))
async def cmd_start(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Привет! Я эхо-бот. Напиши мне что-нибудь."
    )

@bot.on_message(F.text.exact("регистрация"))
async def start_form(update):
    await fsm.set_state(update, FormState.waiting_for_name)
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Введите ваше имя:"
    )

@bot.on_message()
async def handle_input(update):
    state = await fsm.get_state(update)

    if state == FormState.waiting_for_name:
        await fsm.update_data(update, {"name": update.message.body.text})
        await fsm.set_state(update, FormState.waiting_for_age)
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="Введите ваш возраст:"
        )
    elif state == FormState.waiting_for_age:
        await fsm.update_data(update, {"age": update.message.body.text})
        await fsm.clear(update)
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text=f"Регистрация завершена!\nИмя: {update.message.body.text}"
        )
    else:
        # Эхо для обычных сообщений
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text=f"Вы написали: {update.message.body.text}"
        )

async def main():
    await bot.start()
    await bot.start_polling()
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## См. также

- [Руководства](../guides/installation.md) — полное руководство по использованию
- [Фильтры](../guides/filters.md) — система фильтрации обновлений
- [FSM](../guides/fsm.md) — машина состояний
- [Middleware](../guides/middleware.md) — промежуточная обработка