--- docs/guides/polling.md (原始)


+++ docs/guides/polling.md (修改后)
# Long Polling

Long polling is the simplest way to receive updates from MAX API.

## Basic Usage

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

async def main():
    await bot.start_polling()
```

## Advanced Options

```python
await bot.start_polling(
    timeout=30,           # Long polling timeout
    drop_pending=True,    # Skip pending updates
    allowed_updates=["message", "callback_query"]
)
```

## Graceful Shutdown

```python
import asyncio
import signal

bot = Bot(token="YOUR_TOKEN")

async def shutdown():
    await bot.stop()

loop = asyncio.get_event_loop()
for sig in (signal.SIGTERM, signal.SIGINT):
    loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

loop.run_until_complete(bot.start_polling())
```

## See Also

- [Webhook](webhook.md) - Alternative update method
- [Quick Start](quickstart.md) - Basic bot setup