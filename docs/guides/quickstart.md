--- docs/guides/quickstart.md (原始)


+++ docs/guides/quickstart.md (修改后)
# Quick Start

## Basic Bot Setup

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

@bot.on_message()
async def handle_message(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello, {message.from_user.username}!"
    )

async def main():
    await bot.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Key Concepts

- **Bot**: Main class for interacting with MAX API
- **Handlers**: Functions that process updates
- **Filters**: Conditions for triggering handlers
- **Middleware**: Pre/post-processing of updates

## Next Steps

- [Polling](polling.md) - Long polling setup
- [Webhook](webhook.md) - Webhook configuration
- [Handlers](handlers.md) - Working with handlers