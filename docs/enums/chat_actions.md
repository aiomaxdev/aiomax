# Chat Actions

Действия бота из `aiomax.enums.chat_action_enums.ChatAction`:

- `TYPING`
- `SENDING_PHOTO`
- `SENDING_VIDEO`
- `SENDING_AUDIO`
- `SENDING_FILE`
- `MARK_SEEN`

```python
from aiomax.enums.chat_action_enums import ChatAction

await bot.send_action(chat_id=-100123456, action=ChatAction.TYPING)
```
