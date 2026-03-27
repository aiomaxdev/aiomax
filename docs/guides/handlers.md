# Handlers

Handlers are functions that process incoming updates.

## Registering Handlers

### Decorator Syntax

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

@bot.on_message()
async def handle_message(message):
    await bot.send_message(chat_id=message.chat.id, text="Hello!")
```

### Method Syntax

```python
async def handle_message(message):
    await bot.send_message(chat_id=message.chat.id, text="Hello!")

bot.add_handler(handle_message, event_type="message")
```

## Handler Types

```python
@bot.on_message()           # Text messages
@bot.on_callback_query()    # Callback queries
@bot.on_inline_query()      # Inline queries
@bot.on_chat_member()       # Chat member updates
@bot.on_poll()              # Poll updates
```

## With Filters

```python
from aiomax import filters

@bot.on_message(filters.text)
async def handle_text(message):
    pass

@bot.on_message(filters.command("/start"))
async def handle_start(message):
    pass
```

## Handler Order

Handlers are executed in the order they were registered. First matching handler wins.

```python
@bot.on_message(filters.command("admin"))  # Checked first
async def admin_handler(message):
    pass

@bot.on_message()  # Fallback
async def default_handler(message):
    pass
```

## See Also

- [Filters](filters.md) - Filtering updates
- [Middleware](middleware.md) - Pre/post-processing