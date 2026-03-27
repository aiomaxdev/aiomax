# Update Types

Types of updates that can be received from MAX API.

## Enum Values

```python
from aiomax.enums import UpdateType

UpdateType.MESSAGE          # "message" - New incoming message
UpdateType.EDITED_MESSAGE   # "edited_message" - Edited message
UpdateType.CALLBACK_QUERY   # "callback_query" - Callback from inline button
UpdateType.INLINE_QUERY     # "inline_query" - Inline query
UpdateType.CHAT_MEMBER      # "chat_member" - Chat member changed
UpdateType.POLL             # "poll" - Poll update
UpdateType.POLL_ANSWER      # "poll_answer" - User answered poll
```

## Filtering by Update Type

```python
from aiomax import filters

# All messages
@bot.on_message()
async def handle_message(message):
    pass

# Only edited messages
@bot.on_edited_message()
async def handle_edited(message):
    pass

# Callback queries
@bot.on_callback_query()
async def handle_callback(callback):
    pass

# Inline queries
@bot.on_inline_query()
async def handle_inline(query):
    pass

# Chat member changes
@bot.on_chat_member()
async def handle_member_change(update):
    pass
```

## Allowed Updates

When setting up webhook or polling, you can specify which updates to receive:

```python
# Only receive specific update types
await bot.start_polling(
    allowed_updates=[
        UpdateType.MESSAGE,
        UpdateType.CALLBACK_QUERY
    ]
)

# Or as strings
await bot.set_webhook(
    url="https://example.com/webhook",
    allowed_updates=["message", "callback_query"]
)
```

## Update Type Priority

When multiple handlers match, they are executed in registration order:

```python
# This handler is checked first
@bot.on_message(filters.command("admin"))
async def admin_handler(message):
    pass

# This is the fallback
@bot.on_message()
async def default_handler(message):
    pass
```

## Processing All Updates

```python
@bot.on_update()  # Catches all update types
async def handle_all(update):
    print(f"Received update type: {update.update_type}")

    if update.message:
        await handle_message(update.message)
    elif update.callback_query:
        await handle_callback(update.callback_query)
```

## See Also

- [Handlers](../guides/handlers.md) - Working with handlers
- [Filters](../guides/filters.md) - Filtering updates
- [Chat Types](chat_types.md) - Available chat types