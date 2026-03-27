# Рефакторинг бота для MAX Platform

## Что было сделано

### 1. **Внедрена диспетчеризация как в aiogram**

Диспетчеризация — это механизм распределения входящих событий между обработчиками. В aiogram (и теперь в aiomax) это работает так:

```
Update → Dispatcher → Router → Handler
```

**Зачем это нужно:**
- **Модульность**: Разделение кода на логические блоки (роутеры)
- **Фильтрация**: Автоматический выбор нужного обработчика по типу события, тексту, команде и т.д.
- **Middleware**: Возможность выполнять код до/после обработки (логирование, rate limiting, авторизация)
- **FSM**: Управление состояниями диалога

**Компоненты:**
- `Dispatcher` — центральный диспетчер, управляет всеми событиями
- `Router` — группирует обработчики по темам (например: команды, сообщения, коллбэки)
- `F` — фильтры для событий (Command, Text, ChatID, CallbackData, State)
- `Middleware` — промежуточный слой для обработки событий

### 2. **Добавлена поддержка Webhook**

Теперь бот может работать в двух режимах:

#### Режим Polling (для разработки)
```python
# bot.py запускается локально и сам опрашивает сервер MAX
await dp.start_polling(bot, limit=100, timeout=30)
```

#### Режим Webhook (для production)
```python
# На вашем сервере поднимается HTTP-сервер
# MAX отправляет события на ваш endpoint при их появлении
runner = await start_webhook_app()
```

**Для настройки webhook выполните:**
```bash
curl -X POST 'https://platform-api.max.ru/subscriptions' \
  -H 'Authorization: YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-domain.com/webhook", "secret": "your_secret"}'
```

### 3. **Структура проекта**

```
/workspace/
├── bot.py              # Главный файл бота с обработчиками
├── config.py           # Конфигурация (токены, URL, порты)
├── .env                # Переменные окружения (не коммитить!)
├── requirements.txt    # Зависимости
└── aiomax/             # Библиотека aiomax
    ├── client/         # Клиент для API MAX
    ├── handlers/       # Диспетчеризация (aiogram-style)
    │   ├── dispatcher.py
    │   ├── router.py
    │   ├── filters.py
    │   ├── fsm.py
    │   └── middleware.py
    └── ...
```

## Чего не хватает для работы

### 1. Установите зависимости

```bash
pip install aiohttp python-dotenv
```

Или используйте готовый `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Настройте переменные окружения

Создайте файл `.env` в корне проекта:

```env
MaxToken=YOUR_BOT_TOKEN_HERE
WEBHOOK_URL=  # Оставьте пустым для polling, или укажите https://your-domain.com/webhook
WEBHOOK_SECRET=my_super_secret_key
HOST=0.0.0.0
PORT=8080
```

**Где взять токен:**
- Платформа MAX → Чат-боты → Интеграция → Получить токен

### 3. Запуск бота

#### Для разработки (Polling):
```bash
# WEBHOOK_URL должен быть пустым в .env
python bot.py
```

#### Для production (Webhook):
```bash
# 1. Укажите ваш домен в .env:
# WEBHOOK_URL=https://your-domain.com/webhook

# 2. Запустите бота:
python bot.py

# 3. Настройте webhook через API MAX:
curl -X POST 'https://platform-api.max.ru/subscriptions' \
  -H 'Authorization: YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-domain.com/webhook", "secret": "my_super_secret_key"}'
```

## Примеры использования диспетчеризации

### Создание роутеров по модулям

```python
from aiomax import Router, F

# admin_router.py
admin_router = Router(name="admin")

@admin_router.on_message(F.Command("/ban"))
async def ban_user(event, context):
    # Только админы
    ...

# user_router.py
user_router = Router(name="user")

@user_router.on_message(F.Text("привет"))
async def hello(event, context):
    ...

# main.py
dp.include_router(admin_router)
dp.include_router(user_router)
```

### Фильтры

```python
# По команде
@router.on_message(F.Command("/start"))

# По тексту
@router.on_message(F.Text("привет"))
@router.on_message(F.Text(contains="спасибо"))
@router.on_message(F.Text(startswith="/"))

# По ID чата/пользователя
@router.on_message(F.ChatID(-100123456789))
@router.on_message(F.UserID(123456789))

# По состоянию FSM
@router.on_message(F.State("waiting_for_name"))

# Комбинация фильтров
@router.on_message(F.Command("/pay"), F.ChatID(-100123456789))
```

### Middleware

```python
from aiomax import Middleware

class AuthMiddleware(Middleware):
    async def __call__(self, event, context, call_next):
        user_id = event.get("message", {}).get("sender", {}).get("user_id")
        
        if not is_authorized(user_id):
            return  # Игнорируем событие
        
        context["user"] = get_user(user_id)
        return await call_next(event, context)

dp.add_middleware(AuthMiddleware())
dp.add_middleware(LoggingMiddleware())
dp.add_middleware(RateLimitMiddleware(rate=10, window=60))
```

### FSM (Машина состояний)

```python
from aiomax import State, StatesGroup, F

class FormState(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()

@router.on_message(F.Command("/form"))
async def start_form(event, context):
    await context["fsm"].set_state(FormState.waiting_for_name)
    await bot.send_message(chat_id=..., text="Введите ваше имя:")

@router.on_message(F.State(FormState.waiting_for_name))
async def process_name(event, context):
    name = event["message"]["body"]["text"]
    context["fsm"].update_data({"name": name})
    await context["fsm"].set_state(FormState.waiting_for_age)
    await bot.send_message(chat_id=..., text="Введите возраст:")

@router.on_message(F.State(FormState.waiting_for_age))
async def process_age(event, context):
    age = event["message"]["body"]["text"]
    data = await context["fsm"].get_data()
    # Сохраняем данные: data["name"], age
    await context["fsm"].clear()
```

## Отличия Webhook от Polling

| Характеристика | Polling | Webhook |
|---------------|---------|---------|
| **Как работает** | Бот сам опрашивает сервер | Сервер сам отправляет события боту |
| **Задержка** | Есть (зависит от timeout) | Мгновенная |
| **Нагрузка** | Постоянные запросы к API | Только при событиях |
| **Сложность** | Простая настройка | Нужен HTTPS сервер |
| **Для чего** | Разработка, тесты | Production |
| **Порт** | Не требуется | 443 (HTTPS) |

## Рекомендации

1. **Для разработки** используйте Polling — проще и быстрее
2. **Для production** используйте Webhook — меньше задержки, меньше нагрузка
3. **Всегда используйте `WEBHOOK_SECRET`** для проверки подлинности запросов
4. **Разделяйте код на роутеры** по функциональности (админка, пользователи, платежи)
5. **Добавьте логирование** через `LoggingMiddleware`
6. **Ограничьте частоту запросов** через `RateLimitMiddleware`
