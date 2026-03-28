# Chats

Методы для работы с чатами.

## get_chats

Получить список чатов, доступных боту.

```python
chats = await bot.get_chats()
```

## get_chat_info_by_chat_id

Получить информацию о конкретном чате.

```python
chat = await bot.get_chat_info_by_chat_id(chat_id=-100123456)
print(chat.title)
```

## patch_chat_info_by_chat_id

Изменить поля чата (например, заголовок).

```python
updated = await bot.patch_chat_info_by_chat_id(
    chat_id=-100123456,
    title="Новое название"
)
```

## delete_chat_by_chat_id

Удалить чат.

```python
await bot.delete_chat_by_chat_id(chat_id=-100123456)
```

## send_action

Отправить действие в чат (например, typing).

```python
await bot.send_action(
    chat_id=-100123456,
    action="typing"
)
```

## delete_bot_from_chat

Удалить бота из чата.

```python
await bot.delete_bot_from_chat(chat_id=-100123456)
```

## See Also

- [Members](members.md) - участники
- [Admins](admins.md) - администраторы
