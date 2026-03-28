# Keyboard Models

Модели клавиатур находятся в `aiomax.models.keyboard` и
`aiomax.models.attachments.inline_keyboard`.

Пример: обработка callback нажатия кнопки.

```python
from aiomax.filters import F

@bot.on_callback(F.callback.contains("vote:"))
async def vote(update):
    await bot.answer_callback(
        callback_id=update.callback.callback_id,
        notification="Голос принят"
    )
```
