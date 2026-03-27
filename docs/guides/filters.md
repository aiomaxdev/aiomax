--- docs/guides/filters.md (原始)


+++ docs/guides/filters.md (修改后)
# Filters

Filters determine which updates should be processed by a handler.

## Built-in Filters

```python
from aiomax import filters

# Message type filters
filters.text
filters.photo
filters.video
filters.audio
filters.document
filters.sticker
filters.animation
filters.voice
filters.contact
filters.location

# Command filter
filters.command("/start")
filters.command(["/start", "/help"])

# Chat type filters
filters.private
filters.group
filters.channel

# User filters
filters.user(user_id)
filters.user([user_id1, user_id2])
```

## Custom Filters

```python
from aiomax import filters

class IsAdmin(filters.BaseFilter):
    async def check(self, message):
        return message.from_user.id == ADMIN_ID

@bot.on_message(IsAdmin())
async def admin_only(message):
    pass
```

## Combining Filters

```python
# AND
filters.text & filters.private

# OR
filters.command("/start") | filters.command("/help")

# NOT
~filters.bot

# Complex
(filters.text | filters.photo) & filters.private & ~filters.bot
```

## Regex Filter

```python
import re

@bot.on_message(filters.regex(r'^/ban\s+(\d+)'))
async def ban_user(message):
    user_id = message.matches.group(1)
```

## See Also

- [Handlers](handlers.md) - Working with handlers