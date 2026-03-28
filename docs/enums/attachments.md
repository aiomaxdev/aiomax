# Attachments

Типы вложений определены в `AttachmentType`:

- `IMAGE`
- `VIDEO`
- `AUDIO`
- `FILE`
- `STICKER`
- `CONTACT`
- `INLINE_KEYBOARD`
- `SHARE`
- `LOCATION`

```python
from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.filters import F

@bot.on_message(F.content(AttachmentType.IMAGE))
async def on_image(update):
    ...
```
