--- docs/models/chat.md (原始)


+++ docs/models/chat.md (修改后)
# Chat

Represents a chat in MAX messenger.

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique chat identifier |
| `type` | `str` | Chat type: `private`, `group`, `supergroup`, `channel` |
| `title` | `str` | Chat title (for groups/channels) |
| `username` | `str` | Chat username (if public) |
| `first_name` | `str` | First name (for private chats) |
| `last_name` | `str` | Last name (for private chats) |
| `photo` | `ChatPhoto` | Chat photo (if set) |
| `description` | `str` | Chat description (for groups/channels) |

## Chat Types

```python
from aiomax.enums import ChatType

ChatType.PRIVATE      # "private"
ChatType.GROUP        # "group"
ChatType.SUPERGROUP   # "supergroup"
ChatType.CHANNEL      # "channel"
```

## Methods

### `get_members()`

Get list of chat members.

```python
members = await chat.get_members()
for member in members:
    print(member.user.username)
```

### `get_member(user_id)`

Get a specific chat member.

```python
member = await chat.get_member(user_id=123456)
print(member.status)  # "administrator", "member", etc.
```

### `kick_member(user_id)`

Kick a member from the chat.

```python
await chat.kick_member(user_id=123456)
```

### `ban_member(user_id)`

Ban a member from the chat.

```python
await chat.ban_member(user_id=123456)
```

### `unban_member(user_id)`

Unban a previously banned member.

```python
await chat.unban_member(user_id=123456)
```

### `set_description(description)`

Set chat description.

```python
await chat.set_description("Welcome to our group!")
```

### `set_photo(photo)`

Set chat photo.

```python
with open("photo.jpg", "rb") as f:
    await chat.set_photo(photo=f)
```

### `delete_photo()`

Delete chat photo.

```python
await chat.delete_photo()
```

## Example

```python
@bot.on_message(filters.group)
async def handle_group(message):
    chat = message.chat

    if chat.type == "supergroup":
        await bot.send_message(
            chat_id=chat.id,
            text=f"Welcome to {chat.title}!"
        )
```

## See Also

- [Message](message.md) - Message object
- [User](user.md) - User object
- [Chat Actions](../enums/chat_actions.md) - Available chat actions