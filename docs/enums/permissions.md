--- docs/enums/permissions.md (原始)


+++ docs/enums/permissions.md (修改后)
# Permissions

Chat permissions for members.

## ChatPermissions

Control what regular members can do in a chat.

```python
from aiomax.types import ChatPermissions

# Restrictive permissions (read-only)
readonly = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)

# Full permissions
full = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,  # Usually false for regular members
    can_invite_users=True,
    can_pin_messages=False  # Usually false for regular members
)
```

## Permission Fields

| Field | Description |
|-------|-------------|
| `can_send_messages` | Send text messages |
| `can_send_media_messages` | Send photos, videos, etc. |
| `can_send_polls` | Send polls |
| `can_send_other_messages` | Send stickers, GIFs, etc. |
| `can_add_web_page_previews` | Add link previews |
| `can_change_info` | Change chat info (title, photo, etc.) |
| `can_invite_users` | Invite new members |
| `can_pin_messages` | Pin messages |

## Applying Permissions

### Mute a Member

```python
from aiomax.types import ChatPermissions

await bot.restrict_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    permissions=ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    ),
    until_date=3600  # 1 hour
)
```

### Unmute a Member

```python
from aiomax.types import ChatPermissions

await bot.restrict_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )
)
```

### Set Default Chat Permissions

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

## Administrator Rights

Separate from member permissions, admins have additional rights:

```python
await bot.promote_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    can_delete_messages=True,
    can_restrict_members=True,
    can_promote_members=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=True
)
```

## Checking Permissions

```python
member = await bot.get_chat_member(chat_id, user_id)

if not member.can_send_messages:
    print("User is muted")

if member.can_restrict_members:
    print("User can restrict others")
```

## Common Permission Presets

```python
from aiomax.types import ChatPermissions

# Read-only mode
READONLY = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False
)

# No media (text only)
TEXT_ONLY = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=True
)

# Standard member
MEMBER = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True
)
```

## See Also

- [Members](../methods/members.md) - Member management
- [Admins](../methods/admins.md) - Admin rights
- [Chats](../methods/chats.md) - Chat management