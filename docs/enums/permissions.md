# Permissions

Права администраторов чата из `ChatAdminPermission`:

- `READ_ALL_MESSAGES`
- `ADD_REMOVE_MEMBERS`
- `ADD_ADMINS`
- `CHANGE_CHAT_INFO`
- `PIN_MESSAGE`
- `WRITE`
- `EDIT`
- `DELETE`
- и др.

```python
from aiomax.enums.permissions import ChatAdminPermission

await bot.add_admins_to_chat(
    chat_id=-100123456,
    user_id=111,
    permissions=[ChatAdminPermission.WRITE, ChatAdminPermission.DELETE]
)
```
