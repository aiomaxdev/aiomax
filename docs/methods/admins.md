--- docs/methods/admins.md (原始)


+++ docs/methods/admins.md (修改后)
# Admins

Methods for managing chat administrators.

## get_chat_administrators

Get list of all administrators in a chat.

```python
admins = await bot.get_chat_administrators(chat_id=chat_id)

for admin in admins:
    user = admin.user
    status = admin.status
    print(f"@{user.username}: {status}")
```

## Administrator Rights

```python
from aiomax.types import ChatAdministratorRights

rights = ChatAdministratorRights(
    is_anonymous=False,
    can_manage_chat=True,
    can_delete_messages=True,
    can_manage_video_chats=True,
    can_restrict_members=True,
    can_promote_members=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=True,
    can_post_messages=True,      # For channels
    can_edit_messages=True,     # For channels
    can_post_stories=True,      # Stories support
    can_edit_stories=True,
    can_delete_stories=True
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
    can_manage_video_chats=True,
    can_restrict_members=True,
    can_promote_members=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=True
)
```

## For Channels

```python
# Channel-specific rights
await bot.promote_chat_member(
    chat_id=channel_id,
    user_id=user_id,
    can_post_messages=True,     # Can post in channel
    can_edit_messages=True,     # Can edit posts
    can_delete_messages=True,
    can_invite_users=True
)
```

## set_chat_administrator_custom_title

Set custom title for an administrator.

```python
await bot.set_chat_administrator_custom_title(
    chat_id=chat_id,
    user_id=user_id,
    custom_title="Moderator"
)
```

## demote_chat_member

Demote an administrator to regular member.

```python
await bot.promote_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    can_manage_chat=False,
    can_delete_messages=False,
    can_restrict_members=False,
    can_invite_users=False,
    can_pin_messages=False
)
```

## Checking Admin Status

```python
member = await bot.get_chat_member(chat_id, user_id)

if member.status == "administrator":
    print("User is admin")

    # Check specific rights
    if member.can_delete_messages:
        print("Can delete messages")

    if member.can_restrict_members:
        print("Can restrict members")
```

## Owner vs Administrator

```python
member = await bot.get_chat_member(chat_id, user_id)

if member.status == "creator":
    print("User is the owner (creator)")
elif member.status == "administrator":
    print("User is an administrator")
```

## See Also

- [Chats](chats.md) - Chat management
- [Members](members.md) - Member operations