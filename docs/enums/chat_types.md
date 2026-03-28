# Chat Types

Типы чатов из `aiomax.enums.chat_type.ChatType`:

- `ChatType.DIALOG` — личный диалог
- `ChatType.CHAT` — групповой чат
- `ChatType.CHANNEL` — канал

```python
from aiomax.enums.chat_type import ChatType

if chat.type == ChatType.CHANNEL:
    print("Это канал")
```
