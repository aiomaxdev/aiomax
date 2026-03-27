--- docs/enums/chat_actions.md (原始)


+++ docs/enums/chat_actions.md (修改后)
# Chat Actions

Status indicators shown to users when bot is performing an action.

## Enum Values

```python
from aiomax.enums import ChatAction

ChatAction.TYPING          # Typing text message
ChatAction.UPLOAD_PHOTO    # Uploading photo
ChatAction.RECORD_VIDEO    # Recording video
ChatAction.UPLOAD_VIDEO    # Uploading video
ChatAction.RECORD_VOICE    # Recording voice message
ChatAction.UPLOAD_VOICE    # Uploading voice message
ChatAction.UPLOAD_DOCUMENT # Uploading document
ChatAction.CHOOSE_STICKER  # Choosing sticker
ChatAction.FIND_LOCATION   # Finding location
ChatAction.RECORD_VIDEO_NOTE  # Recording video note
ChatAction.UPLOAD_VIDEO_NOTE  # Uploading video note
```

## Usage

Show typing status while processing:

```python
@bot.on_message()
async def handle(message):
    # Show typing
    await bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    # Process message
    response = await process_message(message.text)

    # Send response
    await bot.send_message(
        chat_id=message.chat.id,
        text=response
    )
```

## Long Operations

For long operations, send chat action periodically:

```python
import asyncio

@bot.on_message()
async def handle(message):
    # Start typing indicator
    await bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    # Simulate long operation
    for i in range(5):
        await asyncio.sleep(1)
        # Refresh typing indicator every few seconds
        await bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING
        )

    await bot.send_message(
        chat_id=message.chat.id,
        text="Operation complete!"
    )
```

## Media Upload Actions

```python
# Before sending photo
await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.UPLOAD_PHOTO
)
await bot.send_photo(chat_id=chat_id, photo=photo)

# Before sending video
await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.UPLOAD_VIDEO
)
await bot.send_video(chat_id=chat_id, video=video)

# Before sending document
await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.UPLOAD_DOCUMENT
)
await bot.send_document(chat_id=chat_id, document=file)

# Before sending voice
await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.UPLOAD_VOICE
)
await bot.send_voice(chat_id=chat_id, voice=audio)
```

## Recording Actions

Use recording actions when generating content:

```python
# When generating voice message
await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.RECORD_VOICE
)
# Generate and send voice...

# When generating video
await bot.send_chat_action(
    chat_id=chat_id,
    action=ChatAction.RECORD_VIDEO
)
# Generate and send video...
```

## Context Manager

Create a context manager for automatic chat actions:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def typing(bot, chat_id):
    await bot.send_chat_action(
        chat_id=chat_id,
        action=ChatAction.TYPING
    )
    try:
        yield
    finally:
        pass  # Action automatically clears when message is sent

# Usage
@bot.on_message()
async def handle(message):
    async with typing(bot, message.chat.id):
        response = await generate_response(message.text)
        await bot.send_message(
            chat_id=message.chat.id,
            text=response
        )
```

## Duration

Chat actions are automatically cleared after:
- Sending a message
- 25 seconds timeout
- Another chat action

## See Also

- [Messages](../methods/messages.md) - Message methods
- [General Methods](../methods/general.md) - General utility methods