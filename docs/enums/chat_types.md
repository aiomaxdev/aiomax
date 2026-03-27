--- docs/enums/chat_types.md (原始)


+++ docs/enums/chat_types.md (修改后)
# Chat Types

Available chat types in MAX messenger.

## Enum Values

```python
from aiomax.enums import ChatType

ChatType.PRIVATE      # "private" - Private chat with a user
ChatType.GROUP        # "group" - Basic group chat
ChatType.SUPERGROUP   # "supergroup" - Supergroup with advanced features
ChatType.CHANNEL      # "channel" - Broadcast channel
```

## Checking Chat Type

```python
@bot.on_message()
async def handle(message):
    chat = message.chat

    if chat.type == ChatType.PRIVATE:
        await message.reply("This is a private chat")

    elif chat.type == ChatType.GROUP:
        await message.reply("This is a basic group")

    elif chat.type == ChatType.SUPERGROUP:
        await message.reply("This is a supergroup")

    elif chat.type == ChatType.CHANNEL:
        await message.reply("This is a channel")
```

## Filter by Chat Type

```python
from aiomax import filters

# Private chats only
@bot.on_message(filters.private)
async def handle_private(message):
    pass

# Groups only (includes supergroups)
@bot.on_message(filters.group)
async def handle_group(message):
    pass

# Channels only
@bot.on_message(filters.channel)
async def handle_channel(message):
    pass
```

## Chat Type Features

| Feature | Private | Group | Supergroup | Channel |
|---------|---------|-------|------------|---------|
| Members | 2 | Up to 200 | Unlimited | Unlimited subscribers |
| Admins | N/A | Yes | Yes with rights | Yes with rights |
| History | Full | Full | Full | Optional |
| Usernames | Yes | Yes | Yes | Yes |
| Links | N/A | Invite links | Invite links | Public links |

## See Also

- [Chat Model](../models/chat.md) - Chat object details
- [Update Types](update_types.md) - Types of updates