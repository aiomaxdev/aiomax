# Admins

Методы для работы с администраторами чата.

## get_admins_from_chat

Получить список администраторов.

```python
admins = await bot.get_admins_from_chat(chat_id=-100123456)
for admin in admins.members:
    print(admin.user_id)
```

## add_admins_to_chat

Назначить пользователя администратором.

```python
await bot.add_admins_to_chat(
    chat_id=-100123456,
    user_id=111,
    permissions=["WRITE", "PIN"]
)
```

## delete_permissions_from_chat

Снять права администратора/права пользователя в чате.

```python
await bot.delete_permissions_from_chat(
    chat_id=-100123456,
    user_id=111
)
```

## See Also

- [Members](members.md)
