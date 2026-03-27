# aiomax Documentation

Добро пожаловать в документацию **aiomax** — современного асинхронного фреймворка для создания ботов в мессенджере MAX.

## 📖 О проекте

**aiomax** — это мощный и гибкий фреймворк для разработки Telegram-подобных ботов с поддержкой:

- ✅ **Асинхронности** — построено на asyncio и aiohttp
- ✅ **Диспетчеризации событий** — удобные декораторы для обработки сообщений, callback и других событий
- ✅ **Фильтров** — гибкая система фильтрации по тексту, командам, чатам, пользователям и типу контента
- ✅ **FSM (Finite State Machine)** — управление состояниями для многошаговых диалогов
- ✅ **Webhook и Polling** — поддержка обоих режимов получения обновлений
- ✅ **Типизации** — полная типизация всех методов и моделей

## 🚀 Быстрый старт

```python
import asyncio
from aiomax import Bot, F

bot = Bot(token="YOUR_TOKEN")

@bot.on_message(F.text.contains("привет"))
async def handle_hello(update):
    await bot.send_message(
        chat_id=update.message.recipient.chat_id,
        text="Привет! Как дела?"
    )

async def main():
    await bot.start()
    await bot.start_polling()
    await bot.close()

asyncio.run(main())
```

## 📚 Разделы документации

### Руководства
Изучите основы работы с фреймворком:

- [Установка](guides/installation.md) — установка библиотеки
- [Быстрый старт](guides/quickstart.md) — первое знакомство
- [Long Polling](guides/polling.md) — получение обновлений через опрос
- [Webhook](guides/webhook.md) — получение обновлений через вебхук
- [Обработчики](guides/handlers.md) — создание обработчиков событий
- [Фильтры](guides/filters.md) — фильтрация обновлений
- [FSM](guides/fsm.md) — машина состояний для диалогов
- [Middleware](guides/middleware.md) — промежуточная обработка
- [Примеры](guides/examples.md) — готовые примеры ботов

### Модели данных
Описание структур данных:

- [Сообщение](models/message.md) — модель сообщения
- [Чат](models/chat.md) — модель чата
- [Пользователь](models/user.md) — модель пользователя
- [Обновление](models/update.md) — модель обновления
- [Webhook](models/webhook.md) — информация о вебхуке
- [Клавиатура](models/keyboard.md) — модели клавиатур
- [Вложения](models/attachments.md) — типы вложений

### API Методы
Документация по методам API:

- [Общие](methods/general.md) — базовые методы
- [Сообщения](methods/messages.md) — работа с сообщениями
- [Чаты](methods/chats.md) — управление чатами
- [Участники](methods/members.md) — управление участниками
- [Администраторы](methods/admins.md) — права администраторов
- [Закрепления](methods/pins.md) — закреплённые сообщения
- [Вебхуки](methods/webhooks.md) — управление подписками

### Перечисления (Enums)
Типы и константы:

- [Типы чатов](enums/chat_types.md)
- [Типы обновлений](enums/update_types.md)
- [Типы кнопок](enums/buttons.md)
- [Типы вложений](enums/attachments.md)
- [Права доступа](enums/permissions.md)
- [Действия с чатом](enums/chat_actions.md)

## 🔗 Полезные ссылки

- [GitHub репозиторий](https://github.com/aiomaxdev/aiomax)
- [PyPI пакет](https://pypi.org/project/aiomax/)

## 📞 Поддержка

Если у вас возникли вопросы или проблемы, создайте issue на GitHub или присоединяйтесь к нашему сообществу.