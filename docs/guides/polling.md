# Long Polling

Long polling — способ получать обновления без внешнего веб-сервера.

## Базовый сценарий

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

async def main():
    await bot.start()
    await bot.start_polling(limit=100, timeout=30)
```

## Фильтрация по типам обновлений

```python
await bot.start_polling(
    limit=100,
    timeout=30,
    types=["message_created", "message_callback"]
)
```

## Рекомендация по остановке

Для остановки polling завершите задачу `start_polling` и затем вызовите `await bot.close()`.
