# Handlers

Handlers — это async-функции, которые принимают объект `Update`.

## Регистрация через декораторы

```python
from aiomax.filters import F

@bot.on_message(F.text.contains("привет"))
async def on_message(update):
    await bot.send_message(chat_id=update.chat_id, text="Привет!")

@bot.on_callback(F.callback.contains("ok"))
async def on_callback(update):
    await bot.answer_callback(callback_id=update.callback.callback_id, notification="OK")
```

## Другие типы обработчиков

```python
@bot.on_bot_started()
async def started(update):
    ...

@bot.on_message_edited()
async def edited(update):
    ...

@bot.on_message_removed()
async def removed(update):
    ...
```

## Регистрация через `register_handler`

```python
from aiomax.enums.update_type import UpdateTypeEnum

async def custom_handler(update):
    ...

bot.register_handler(UpdateTypeEnum.MESSAGE_CREATED, custom_handler)
```
