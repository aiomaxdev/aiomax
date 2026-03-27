--- docs/methods/general.md (原始)


+++ docs/methods/general.md (修改后)
# General Methods

General utility methods for the bot.

## get_me

Get information about the bot.

```python
me = await bot.get_me()
print(f"Bot username: @{me.username}")
print(f"Bot name: {me.first_name}")
print(f"Bot ID: {me.id}")
```

## get_updates

Get updates from the server (for manual polling).

```python
updates = await bot.get_updates(
    offset=0,
    limit=100,
    timeout=30,
    allowed_updates=["message", "callback_query"]
)

for update in updates:
    await bot.process_update(update)
```

## delete_message

Delete a message.

```python
await bot.delete_message(
    chat_id=chat_id,
    message_id=message_id
)

# Or using Message object
await message.delete()
```

## copy_message

Copy a message to another chat.

```python
await bot.copy_message(
    chat_id=dest_chat_id,
    from_chat_id=source_chat_id,
    message_id=message_id
)
```

## forward_message

Forward a message to another chat.

```python
await bot.forward_message(
    chat_id=dest_chat_id,
    from_chat_id=source_chat_id,
    message_id=message_id
)
```

## send_chat_action

Send typing or other status.

```python
from aiomax.enums import ChatAction

await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.TYPING  # or UPLOAD_PHOTO, RECORD_VIDEO, etc.
)
```

## See Also

- [Messages](messages.md) - Message-related methods
- [Chats](chats.md) - Chat management methods