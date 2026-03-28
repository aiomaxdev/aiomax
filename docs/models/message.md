# Message Model

`Message` содержит тело сообщения (`body`), автора и служебные поля.

```python
@bot.on_message()
async def show_message(update):
    msg = update.message
    if msg and msg.body and msg.body.text:
        print(msg.body.text)
```

Получение сообщения через API:

```python
message = await bot.get_message(chat_id=-100123456, message_id="msg-123")
```
