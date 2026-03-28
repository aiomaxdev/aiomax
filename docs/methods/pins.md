# Pins

Методы для закреплённых сообщений.

## pin_message

Закрепить сообщение.

```python
await bot.pin_message(
    chat_id=-100123456,
    message_id="msg-123"
)
```

## unpin_message

Открепить сообщение.

```python
await bot.unpin_message(
    chat_id=-100123456,
    message_id="msg-123"
)
```

## get_pinned_message

Получить текущее закреплённое сообщение чата.

```python
pinned = await bot.get_pinned_message(chat_id=-100123456)
print(pinned.body.text)
```

## See Also

- [Messages](messages.md)
