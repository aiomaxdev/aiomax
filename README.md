**aiomax** — асинхронный Python-клиент для работы с API мессенджера **MAX**.

Библиотека построена на:

- `asyncio`
- `aiohttp`
- `pydantic`

Она предоставляет удобный интерфейс для работы с чатами, сообщениями и событиями бота.

---

# Установка

```bash
pip install aiomax
````

или из исходников

```bash
git clone https://github.com/aiomaxdev/aiomax
cd aiomax
pip install -e .
```

---

# Быстрый старт

```python
import asyncio
from aiomax.client.bot import Bot

TOKEN = "YOUR_TOKEN"

async def main():
    bot = Bot(TOKEN)

    await bot.start()

    me = await bot.get_me()
    print(me)

    chats = await bot.get_chats()
    print(chats)

    await bot.close()

asyncio.run(main())
```

---

# Архитектура

Библиотека построена по слоистой архитектуре.

```
Bot
 │
 ├── API Methods
 │       ├── GetMe
 │       ├── GetChats
 │       ├── SendMessage
 │       └── GetUpdates
 │
 ├── MAXClient
 │       └── aiohttp HTTP client
 │
 └── Models
         ├── Chat
         ├── Message
         ├── User
         └── Updates
```

### Компоненты

| Компонент   | Описание                            |
| ----------- | ----------------------------------- |
| Bot         | основной интерфейс для разработчика |
| MAXClient   | HTTP клиент для API                 |
| API Methods | классы методов API                  |
| Models      | Pydantic модели данных              |

---

# Работа с ботом

## Создание клиента

```python
bot = Bot("TOKEN")
```

---

## Запуск

```python
await bot.start()
```

---

## Закрытие

```python
await bot.close()
```

---

# Методы API

## Получить информацию о боте

```python
bot_info = await bot.get_me()
```

Возвращает:

```
BotInfo
```

---

## Получить список чатов

```python
chats = await bot.get_chats()
```

Возвращает:

```
Chats
```

---

## Получить информацию о чате

```python
chat = await bot.get_chat_info_by_chat_id(
    chat_id=-123456
)
```

Возвращает:

```
Chat
```

---

## Изменить информацию о чате

```python
chat = await bot.patch_chat_info_by_chat_id(
    chat_id=-123456,
    title="New title"
)
```

---

## Удалить чат

```python
await bot.delete_chat_by_chat_id(
    chat_id=-123456
)
```

---

## Отправить сообщение

```python
await bot.send_message(
    chat_id=-123456,
    text="Hello world"
)
```

---

## Получить сообщения

```python
messages = await bot.get_messages(
    chat_id=-123456
)
```

---

# Polling (получение событий)

Библиотека поддерживает **long polling** для получения событий.

```python
async for update in bot.start_polling():
    print(update)
```

---

## Остановка polling

```python
await bot.stop_polling()
```

---

# Как работает polling

```
Bot
 │
 ├── get_updates()
 │
 ├── API возвращает события
 │
 ├── сохраняется marker
 │
 └── возвращаются новые события
```

Алгоритм:

1. бот отправляет `get_updates`
2. API возвращает список событий
3. сохраняется `marker`
4. следующий запрос получает только новые события

---

# Пример простого бота

```python
import asyncio
from aiomax.client.bot import Bot

TOKEN = "TOKEN"

async def main():
    bot = Bot(TOKEN)

    await bot.start()

    async for update in bot.start_polling():

        if update["type"] == "message":

            chat_id = update["message"]["chat_id"]

            await bot.send_message(
                chat_id=chat_id,
                text="Hello from aiomax!"
            )

asyncio.run(main())
```

---

# Модели данных

Библиотека использует **Pydantic** для валидации данных.

Пример модели чата:

```python
class Chat(BaseModel):
    chat_id: int
    title: str
    type: ChatType
    participants_count: int
    icon: ChatIcon | None = None
```

---

# Асинхронность

Все методы библиотеки являются **асинхронными**.

```python
await bot.send_message(...)
```

Это позволяет:

* обрабатывать тысячи сообщений
* не блокировать event loop
* масштабировать ботов

---

# Зависимости

Основные зависимости:

```
aiohttp
pydantic
asyncio
```

---

# Планы развития

* Webhook поддержка
* Router система
* Middleware
* FSM
* Фильтры сообщений
* Типизированные события

---

# Лицензия

MIT

```
