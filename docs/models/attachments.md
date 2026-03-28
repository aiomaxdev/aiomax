# Attachments Model

Вложения приходят в `update.message.body.attachments`.

```python
@bot.on_message()
async def inspect(update):
    if update.message and update.message.body:
        for att in update.message.body.attachments or []:
            print(att)
```

Фильтрация по типу вложения:

```python
from aiomax.filters import F

@bot.on_message(F.content("image"))
async def on_image(update):
    ...
```
