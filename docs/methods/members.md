--- docs/methods/members.md (原始)


+++ docs/methods/members.md (修改后)
# Members

Methods for working with chat members.

## get_chat_member

Get information about a specific member.

```python
member = await bot.get_chat_member(
    chat_id=chat_id,
    user_id=user_id
)

print(f"User: {member.user.username}")
print(f"Status: {member.status}")
print(f"Joined: {member.joined_date}")
```

## Member Statuses

```python
from aiomax.enums import ChatMemberStatus

ChatMemberStatus.OWNER          # Creator of the chat
ChatMemberStatus.ADMINISTRATOR  # Administrator
ChatMemberStatus.MEMBER         # Regular member
ChatMemberStatus.RESTRICTED     # Restricted user
ChatMemberStatus.LEFT           # Left the chat
ChatMemberStatus.BANNED         # Banned user
```

## Checking Member Status

```python
member = await bot.get_chat_member(chat_id, user_id)

if member.status == "administrator":
    print("User is an admin")

if member.is_member:
    print("User is a member")

if member.can_restrict_members:
    print("User can restrict others")
```

## Restricting Members

```python
from aiomax.types import ChatPermissions

await bot.restrict_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    permissions=ChatPermissions(
        can_send_messages=False,  # Mute
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    ),
    until_date=3600  # 1 hour
)
```

## Unrestricting Members

```python
from aiomax.types import ChatPermissions

# Full permissions
full_perms = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)

await bot.restrict_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    permissions=full_perms
)
```

## Banning Members

```python
# Ban permanently
await bot.ban_chat_member(
    chat_id=chat_id,
    user_id=user_id
)

# Ban for 24 hours
import time
until = int(time.time()) + 86400

await bot.ban_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    until_date=until
)
```

## Unbanning Members

```python
await bot.unban_chat_member(
    chat_id=chat_id,
    user_id=user_id
)
```

## Kicking Members

```python
# Kick (same as ban without until_date)
await bot.kick_chat_member(
    chat_id=chat_id,
    user_id=user_id
)
```

## Getting All Members

```python
# Get all administrators
admins = await bot.get_chat_administrators(chat_id=chat_id)
for admin in admins:
    print(f"{admin.user.username}: {admin.status}")

# Get member count
count = await bot.get_chat_member_count(chat_id=chat_id)
print(f"Total members: {count}")
```

## See Also

- [Chats](chats.md) - Chat management
- [Admins](admins.md) - Admin-specific operations