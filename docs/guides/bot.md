# Bot

`Bot` — основной класс aiomax для работы с MAX API и обработкой обновлений.

## Создание

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")
```

## Жизненный цикл

```python
await bot.start()
# ... работа ...
await bot.close()
```

## Основные API-методы

```python
await bot.get_me()
await bot.get_chats()
await bot.get_chat_info_by_chat_id(chat_id=-100123456)
await bot.patch_chat_info_by_chat_id(chat_id=-100123456, title="New title")
await bot.delete_chat_by_chat_id(chat_id=-100123456)

await bot.send_message(chat_id=-100123456, text="Привет")
await bot.send_action(chat_id=-100123456, action="typing")

await bot.get_message(chat_id=-100123456, message_id="msg-1")
await bot.get_messages(chat_id=-100123456, limit=50)
await bot.edit_message(chat_id=-100123456, message_id="msg-1", text="Updated")
await bot.delete_message(chat_id=-100123456, message_id="msg-1")

await bot.pin_message(chat_id=-100123456, message_id="msg-1")
await bot.unpin_message(chat_id=-100123456, message_id="msg-1")
await bot.get_pinned_message(chat_id=-100123456)
```

## Участники и администраторы

```python
await bot.get_members_from_chat(chat_id=-100123456)
await bot.add_members_to_chat(chat_id=-100123456, user_ids=[111, 222])
await bot.delete_members_from_chat(chat_id=-100123456, user_id=111)
await bot.get_me_from_chat(chat_id=-100123456)

await bot.get_admins_from_chat(chat_id=-100123456)
await bot.add_admins_to_chat(chat_id=-100123456, user_id=111, permissions=["WRITE"])
await bot.delete_permissions_from_chat(chat_id=-100123456, user_id=111)
```

## Polling

```python
await bot.start_polling(limit=100, timeout=30, types=["message_created", "message_callback"])
```

## Webhook

```python
await bot.start_webhook(
    host="0.0.0.0",
    port=8080,
    path="/webhook",
    webhook_url="https://example.com/webhook",
    secret="secret"
)

await bot.get_subscriptions()
await bot.set_subscription(url="https://example.com/webhook")
await bot.delete_subscription(url="https://example.com/webhook")
```

## Декораторы обработчиков

```python
from aiomax.filters import F

@bot.on_message(F.command("start"))
async def on_start(update):
    ...

@bot.on_callback(F.callback.contains("ok"))
async def on_callback(update):
    ...

@bot.on_message_edited()
async def on_edited(update):
    ...

@bot.on_message_removed()
async def on_removed(update):
    ...
```
