# Update Types

Типы обновлений перечислены в `UpdateTypeEnum`.

```python
from aiomax.enums.update_type import UpdateTypeEnum

print(UpdateTypeEnum.MESSAGE_CREATED)
print(UpdateTypeEnum.MESSAGE_CALLBACK)
print(UpdateTypeEnum.MESSAGE_EDITED)
```

Использование с регистрацией обработчика:

```python
async def handler(update):
    ...

bot.register_handler(UpdateTypeEnum.MESSAGE_CREATED, handler)
```
