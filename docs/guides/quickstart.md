# Quick Start

## Минимальный бот

```python
import asyncio
from aiomax import Bot
from aiomax.filters import F

bot = Bot(token="YOUR_TOKEN")

@bot.on_message(F.command("start"))
async def handle_start(update):
    await bot.send_message(
        chat_id=update.chat_id,
        text="Привет! Я бот на aiomax."
    )

@bot.on_message()
async def echo(update):
    if update.message and update.message.body and update.message.body.text:
        await bot.send_message(
            chat_id=update.chat_id,
            text=f"Echo: {update.message.body.text}"
        )

async def main():
    await bot.start()
    await bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

## Ключевые сущности

- **Bot** — основной клиент.
- **Update** — входящее событие.
- **Handlers** — обработчики событий.
- **F** — фабрика фильтров.
