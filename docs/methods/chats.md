--- docs/methods/chats.md (原始)


+++ docs/methods/chats.md (修改后)
# Chats

Methods for managing chats.

## get_chat

Get information about a chat.

```python
chat = await bot.get_chat(chat_id=chat_id)
print(f"Title: {chat.title}")
print(f"Type: {chat.type}")
print(f"Members: {chat.member_count}")
```

## get_chat_administrators

Get list of chat administrators.

```python
admins = await bot.get_chat_administrators(chat_id=chat_id)
for admin in admins:
    print(f"{admin.user.username}: {admin.status}")
```

## get_chat_member_count

Get the number of members in a chat.

```python
count = await bot.get_chat_member_count(chat_id=chat_id)
print(f"Members: {count}")
```

## get_chat_member

Get information about a specific member.

```python
member = await bot.get_chat_member(
    chat_id=chat_id,
    user_id=user_id
)
print(f"Status: {member.status}")
print(f"Until date: {member.until_date}")
```

## kick_chat_member

Kick a user from a chat.

```python
await bot.kick_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    until_date=3600  # Ban for 1 hour
)
```

## unban_chat_member

Unban a previously banned user.

```python
await bot.unban_chat_member(
    chat_id=chat_id,
    user_id=user_id
)
```

## restrict_chat_member

Restrict a user's permissions.

```python
from aiomax.types import ChatPermissions

await bot.restrict_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    ),
    until_date=3600  # Mute for 1 hour
)
```

## promote_chat_member

Promote a user to administrator.

```python
await bot.promote_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    is_anonymous=False,
    can_manage_chat=True,
    can_delete_messages=True,
    can_restrict_members=True,
    can_invite_users=True,
    can_pin_messages=True
)
```

## set_chat_permissions

Set default chat permissions.

```python
from aiomax.types import ChatPermissions

await bot.set_chat_permissions(
    chat_id=chat_id,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )
)
```

## set_chat_title

Set chat title.

```python
await bot.set_chat_title(
    chat_id=chat_id,
    title="New Chat Title"
)
```

## set_chat_description

Set chat description.

```python
await bot.set_chat_description(
    chat_id=chat_id,
    description="New description"
)
```

## set_chat_photo

Set chat photo.

```python
with open("photo.jpg", "rb") as f:
    await bot.set_chat_photo(
        chat_id=chat_id,
        photo=f
    )
```

## delete_chat_photo

Delete chat photo.

```python
await bot.delete_chat_photo(chat_id=chat_id)
```

## pin_chat_message

Pin a message in a chat.

```python
await bot.pin_chat_message(
    chat_id=chat_id,
    message_id=message_id,
    disable_notification=True
)
```

## unpin_chat_message

Unpin a message.

```python
await bot.unpin_chat_message(
    chat_id=chat_id,
    message_id=message_id
)

# Unpin all messages
await bot.unpin_all_chat_messages(chat_id=chat_id)
```

## leave_chat

Leave a chat.

```python
await bot.leave_chat(chat_id=chat_id)
```

## export_chat_invite_link

Export invite link for a chat.

```python
link = await bot.export_chat_invite_link(chat_id=chat_id)
print(f"Invite link: {link}")
```

## create_chat_invite_link

Create a new invite link.

```python
link = await bot.create_chat_invite_link(
    chat_id=chat_id,
    name="Special Link",
    expire_date=3600,
    member_limit=100,
    creates_join_request=False
)
```

## See Also

- [Members](members.md) - Member management
- [Admins](admins.md) - Admin operations