# Update Model

`Update` — базовая модель входящего события.

Обычно используется в обработчиках:

```python
@bot.on_message()
async def on_message(update):
    print(update.type)
    print(update.chat_id)
    print(update.user_id)
```

Для callback:

```python
@bot.on_callback()
async def on_callback(update):
    print(update.callback.payload)
```
