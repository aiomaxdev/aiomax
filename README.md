**aiomax** — асинхронный Python-фреймворк для создания ботов в мессенджере **MAX**.

Библиотека построена на:

- `asyncio`
- `aiohttp`
- `pydantic`

Она предоставляет удобный интерфейс для работы с чатами, сообщениями и событиями бота.

## Основные возможности

- ✅ **Диспетчеризация событий** — декораторы для обработки сообщений, callback и других событий
- ✅ **Фильтры** — гибкая система фильтрации по тексту, командам, чатам, пользователям и типу контента
- ✅ **FSM (Finite State Machine)** — управление состояниями для многошаговых диалогов
- ✅ **Webhook и Polling** — поддержка обоих режимов получения обновлений
- ✅ **Типизация** — полная типизация всех методов и моделей

---

# Установка

```bash
pip install aiomax-python
````

или из исходников

```bash
git clone https://github.com/aiomaxdev/aiomax
cd aiomax
pip install -e .
```

---

# Быстрый старт

## Простой эхо-бот

```python
import asyncio
from aiomax import Bot
from aiomax.filters import F

bot = Bot(token="YOUR_TOKEN")

@bot.on_message(F.text.contains("привет"))
async def handle_hello(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Привет! Как дела?"
    )

@bot.on_message()
async def echo(update):
    if update.message and update.message.body.text:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text=f"Вы написали: {update.message.body.text}"
        )

async def main():
    await bot.start()
    await bot.start_polling()
    await bot.close()

asyncio.run(main())
```

## Бот с командами

```python
from aiomax import Bot
from aiomax.filters import F

bot = Bot(token="YOUR_TOKEN")

@bot.on_message(F.command("start"))
async def cmd_start(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Добро пожаловать!"
    )

@bot.on_message(F.command("help"))
async def cmd_help(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="/start - начать\n/help - помощь"
    )
```

## Бот с FSM (многошаговая форма)

```python
from aiomax import Bot
from aiomax.filters import F
from aiomax.fsm import State, StatesGroup, MemoryStorage, FSMManager

bot = Bot(token="YOUR_TOKEN")
fsm = FSMManager(MemoryStorage())

class FormState(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()

@bot.on_message(F.command("register"))
async def start_register(update):
    await fsm.set_state(update.user_id, str(FormState.waiting_for_name), update.chat_id)
    await bot.send_message(chat_id=update.chat_id, text="Введите имя:")

@bot.on_message()
async def handle_input(update):
    state = await fsm.get_state(update.user_id, update.chat_id)

    if state == FormState.waiting_for_name:
        await fsm.update_data(update.user_id, {"name": update.message.body.text}, update.chat_id)
        await fsm.set_state(update.user_id, str(FormState.waiting_for_age), update.chat_id)
        await bot.send_message(chat_id=update.chat_id, text="Введите возраст:")
    elif state == FormState.waiting_for_age:
        await fsm.update_data(update.user_id, {"age": update.message.body.text}, update.chat_id)
        await fsm.clear(update.user_id, update.chat_id)
        await bot.send_message(chat_id=update.chat_id, text="Регистрация завершена!")
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

# Система фильтров

Фильтры позволяют гибко настраивать условия обработки сообщений:

```python
from aiomax import Bot, F

bot = Bot(token="YOUR_TOKEN")

# Текстовые фильтры
@bot.on_message(F.text.exact("привет"))      # точное совпадение
@bot.on_message(F.text.contains("помощь"))   # содержит текст
@bot.on_message(F.text.startswith("/"))      # начинается с
@bot.on_message(F.text.endswith("!"))        # заканчивается на
@bot.on_message(F.text.regex(r"\d+"))        # regex паттерн

# Команды
@bot.on_message(F.command("start"))          # команда /start
@bot.on_message(F.command("help", prefix="!"))  # команда !help

# Фильтры по чатам и пользователям
@bot.on_message(F.chat(123456))              # только в чате с ID
@bot.on_message(F.user(789012))              # только от пользователя

# Callback данные
@bot.on_callback(F.callback.data("buy"))     # точный callback
@bot.on_callback(F.callback.contains("pay")) # содержит в callback

# Тип контента
@bot.on_message(F.content("image"))          # изображения
@bot.on_message(F.content("video"))          # видео
@bot.on_message(F.content("text"))           # текст

# Комбинирование фильтров
@bot.on_message(F.user(123) & F.text.contains("admin"))  # И
@bot.on_message(F.text.contains("да") | F.text.contains("нет"))  # ИЛИ
@bot.on_message(~F.text.contains("спам"))    # НЕ (инверсия)
```

---

# FSM (Finite State Machine)

Управление состояниями для многошаговых диалогов:

```python
from aiomax import Bot, StatesGroup, State, MemoryStorage, FSMManager

bot = Bot(token="YOUR_TOKEN")
storage = MemoryStorage()
fsm = FSMManager(storage)

# Определение состояний
class FormState(StatesGroup):
    waiting_for_name = "waiting_for_name"
    waiting_for_age = "waiting_for_age"
    waiting_for_email = "waiting_for_email"

# Начало формы
@bot.on_message(F.command("register"))
async def start_registration(update):
    await fsm.set_state(update, FormState.waiting_for_name)
    await bot.send_message(chat_id=..., text="Введите имя:")

# Обработка ввода
@bot.on_message()
async def handle_form_input(update):
    state = await fsm.get_state(update)

    if state == FormState.waiting_for_name:
        data = {"name": update.message.body.text}
        await fsm.update_data(update, data)
        await fsm.set_state(update, FormState.waiting_for_age)

    elif state == FormState.waiting_for_age:
        await fsm.update_data(update, {"age": update.message.body.text})
        await fsm.set_state(update, FormState.waiting_for_email)

    elif state == FormState.waiting_for_email:
        await fsm.update_data(update, {"email": update.message.body.text})
        await fsm.clear(update)  # Очистка состояния
```

---

# Примеры

Примеры ботов находятся в папке `examples/`:

| Файл | Описание |
|------|----------|
| `echo_bot.py` | Простой эхо-бот с фильтрами |
| `fsm_bot.py` | Бот с многошаговой формой регистрации |
| `callback_bot.py` | Бот с inline кнопками и callback |
| `filtered_bot.py` | Бот с фильтрами по чатам и пользователям |

---

# Планы развития

* [x] Диспетчеризация событий
* [x] Фильтры сообщений
* [x] FSM (Finite State Machine)
* [x] Webhook поддержка
* [ ] Router система
* [ ] Middleware цепочки
* [ ] Dependency injection
* [ ] i18n/L10n поддержка

---

# Лицензия

MIT
