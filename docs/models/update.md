# Update

Represents an incoming update from MAX API.

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `update_id` | `int` | Unique update identifier |
| `message` | [`Message`](message.md) | New incoming message (if any) |
| `edited_message` | `Message` | Edited message (if any) |
| `callback_query` | `CallbackQuery` | Callback query (if any) |
| `inline_query` | `InlineQuery` | Inline query (if any) |
| `chat_member` | `ChatMemberUpdated` | Chat member change (if any) |
| `poll` | `Poll` | Poll update (if any) |

## Properties

### `effective_chat`

Get the chat associated with this update.

```python
chat = update.effective_chat
```

### `effective_user`

Get the user associated with this update.

```python
user = update.effective_user
```

### `effective_message`

Get the message associated with this update.

```python
message = update.effective_message
```

## Update Types

```python
from aiomax.enums import UpdateType

UpdateType.MESSAGE          # "message"
UpdateType.EDITED_MESSAGE   # "edited_message"
UpdateType.CALLBACK_QUERY   # "callback_query"
UpdateType.INLINE_QUERY     # "inline_query"
UpdateType.CHAT_MEMBER      # "chat_member"
UpdateType.POLL             # "poll"
```

## Example

```python
@bot.on_update()
async def handle_all_updates(update):
    # Log all updates
    print(f"Received update {update.update_id}")

    # Get effective chat and user
    chat = update.effective_chat
    user = update.effective_user

    if chat and user:
        print(f"From {user.username} in {chat.title}")
```

## Processing Specific Updates

```python
# Message
@bot.on_message()
async def handle_message(message):
    pass

# Callback Query
@bot.on_callback_query()
async def handle_callback(callback):
    pass

# Chat Member
@bot.on_chat_member()
async def handle_member_change(update):
    pass
```

## See Also

- [Message](message.md) - Message object
- [Handlers](../guides/handlers.md) - Working with handlers