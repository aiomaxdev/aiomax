# Pins

Methods for pinning and unpinning messages.

## pin_chat_message

Pin a message in a chat.

```python
await bot.pin_chat_message(
    chat_id=chat_id,
    message_id=message_id,
    disable_notification=True  # Don't notify members
)
```

## unpin_chat_message

Unpin a specific message.

```python
await bot.unpin_chat_message(
    chat_id=chat_id,
    message_id=message_id
)
```

## unpin_all_chat_messages

Unpin all messages in a chat.

```python
await bot.unpin_all_chat_messages(chat_id=chat_id)
```

## Getting Pinned Message

```python
chat = await bot.get_chat(chat_id=chat_id)

if chat.pinned_message:
    print(f"Pinned message ID: {chat.pinned_message.id}")
    print(f"Text: {chat.pinned_message.text}")
```

## Pin with Notification

```python
# Notify all members about the pinned message
await bot.pin_chat_message(
    chat_id=chat_id,
    message_id=message_id,
    disable_notification=False
)
```

## Use Cases

### Pin Welcome Message

```python
@bot.on_message(filters.command("start"))
async def cmd_start(message):
    welcome = await bot.send_message(
        chat_id=message.chat.id,
        text="Welcome to the group!"
    )

    # Pin the welcome message
    await bot.pin_chat_message(
        chat_id=message.chat.id,
        message_id=welcome.id,
        disable_notification=True
    )
```

### Pin Important Announcement

```python
@bot.on_message(filters.command("announce") & filters.admin)
async def announce(message):
    # Forward announcement and pin it
    pinned = await message.reply_to_message.forward(
        chat_id=message.chat.id
    )

    await bot.pin_chat_message(
        chat_id=message.chat.id,
        message_id=pinned.id,
        disable_notification=False
    )
```

### Unpin Old Messages

```python
@bot.on_message(filters.command("clean_pins"))
async def clean_pins(message):
    if not await is_admin(message):
        return

    await bot.unpin_all_chat_messages(
        chat_id=message.chat.id
    )

    await message.reply("All pins cleared!")
```

## See Also

- [Chats](chats.md) - Chat management methods
- [Messages](messages.md) - Message methods