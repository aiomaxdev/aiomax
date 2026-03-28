# Members

Методы для управления участниками чата.

## get_members_from_chat

Получить список участников.

```python
members = await bot.get_members_from_chat(chat_id=-100123456)
```

## add_members_to_chat

Добавить участников в чат.

```python
await bot.add_members_to_chat(
    chat_id=-100123456,
    user_ids=[111, 222, 333]
)
```

## delete_members_from_chat

Удалить участника из чата.

```python
await bot.delete_members_from_chat(
    chat_id=-100123456,
    user_id=111
)
```

## get_me_from_chat

Получить информацию о самом боте как участнике конкретного чата.

```python
me_in_chat = await bot.get_me_from_chat(chat_id=-100123456)
print(me_in_chat.status)
```

## See Also

- [Admins](admins.md)
- [Chats](chats.md)
