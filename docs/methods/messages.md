# Messages

Методы для отправки и управления сообщениями.

## send_message

Отправка сообщения в чат.

```python
result = await bot.send_message(
    chat_id=-100123456,
    text="Привет!"
)
```

## get_message

Получить одно сообщение по идентификатору.

```python
message = await bot.get_message(
    chat_id=-100123456,
    message_id="msg-123"
)
```

## get_messages

Получить список сообщений.

```python
messages = await bot.get_messages(
    chat_id=-100123456,
    limit=50
)
```

## edit_message

Редактировать сообщение.

```python
await bot.edit_message(
    chat_id=-100123456,
    message_id="msg-123",
    text="Обновлённый текст"
)
```

## delete_message

Удалить сообщение.

```python
await bot.delete_message(
    chat_id=-100123456,
    message_id="msg-123"
)
```

## answer_callback

Ответ на callback от inline-кнопки.

```python
await bot.answer_callback(
    callback_id="cb-123",
    notification="Готово"
)
```

## See Also

- [Pins](pins.md) - закреплённые сообщения
