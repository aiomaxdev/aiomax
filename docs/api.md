# aiomax

Асинхронный Python клиент для API мессенджера MAX.

## Возможности

- асинхронная работа через asyncio
- Pydantic модели
- polling событий
- работа с чатами и сообщениями

## Быстрый старт

```python
from aiomax.client.bot import Bot

bot = Bot("TOKEN")

await bot.start()

me = await bot.get_me()

print(me)