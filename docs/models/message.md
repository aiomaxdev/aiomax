--- docs/models/message.md (原始)


+++ docs/models/message.md (修改后)
# Message

Represents a message in MAX messenger.

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique message identifier |
| `chat` | [`Chat`](chat.md) | Chat where the message was sent |
| `from_user` | [`User`](user.md) | Sender of the message |
| `text` | `str` | Text content of the message |
| `date` | `datetime` | Date when the message was sent |
| `reply_to_message` | `Message` | Replied message (if any) |

## Methods

### `reply(text, **kwargs)`

Reply to this message.

```python
@bot.on_message()
async def handle(message):
    await message.reply("Hello!")
```

### `forward(chat_id)`

Forward this message to another chat.

```python
@bot.on_message()
async def handle(message):
    await message.forward(chat_id=ADMIN_CHAT_ID)
```

### `delete()`

Delete this message.

```python
@bot.on_message()
async def handle(message):
    await message.delete()
```

### `edit_text(text)`

Edit the text of this message.

```python
@bot.on_callback_query()
async def handle(callback):
    await callback.message.edit_text("Updated!")
```

## Example

```python
@bot.on_message()
async def echo_with_reply(message):
    # Reply to the message
    await message.reply(f"You said: {message.text}")

    # Access sender info
    username = message.from_user.username

    # Access chat info
    chat_title = message.chat.title
```

## See Also

- [Chat](chat.md) - Chat information
- [User](user.md) - User information
- [Update](update.md) - Update object