# User

Represents a user in MAX messenger.

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique user identifier |
| `is_bot` | `bool` | True if the user is a bot |
| `first_name` | `str` | User's first name |
| `last_name` | `str` | User's last name (optional) |
| `username` | `str` | User's username (optional) |
| `language_code` | `str` | IETF language code (optional) |
| `is_premium` | `bool` | True if the user has premium |
| `added_to_attachment_menu` | `bool` | True if added to attachment menu |

## Methods

### `get_profile_photos()`

Get user's profile photos.

```python
photos = await user.get_profile_photos()
for photo in photos:
    print(photo.file_id)
```

### `send_message(text)`

Send a message to this user.

```python
await user.send_message("Hello!")
```

### `mention_html(name=None)`

Get HTML mention for this user.

```python
mention = user.mention_html()
# Output: <a href="tg://user?id=123">Name</a>

mention = user.mention_html("Custom Name")
# Output: <a href="tg://user?id=123">Custom Name</a>
```

### `mention_markdown(name=None)`

Get Markdown mention for this user.

```python
mention = user.mention_markdown()
# Output: [Name](tg://user?id=123)
```

## Example

```python
@bot.on_message(filters.command("start"))
async def cmd_start(message):
    user = message.from_user

    greeting = f"Hello, {user.first_name}!"

    if user.is_premium:
        greeting += " 🌟"

    await bot.send_message(
        chat_id=user.id,
        text=greeting
    )

    # Send with mention
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{user.mention_html()} started the bot!",
        parse_mode="HTML"
    )
```

## See Also

- [Message](message.md) - Message object
- [Chat](chat.md) - Chat object