# Buttons

Типы кнопок определены в `aiomax.enums.button_type_enum.ButtonType`:

- `CALLBACK`
- `LINK`
- `REQUEST_GEO_LOCATION`
- `REQUEST_CONTACT`
- `OPEN_APP`
- `MESSAGE`

```python
from aiomax.enums.button_type_enum import ButtonType
```

Для обработки callback-кнопок используйте:

```python
from aiomax.filters import F

@bot.on_callback(F.callback.contains("action:"))
async def on_action(update):
    ...
```
