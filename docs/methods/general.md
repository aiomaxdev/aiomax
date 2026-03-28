# General Methods

Базовые методы бота для жизненного цикла и получения обновлений.

## start

Инициализирует HTTP-клиент.

```python
await bot.start()
```

## close

Корректно завершает работу бота и закрывает клиент.

```python
await bot.close()
```

## get_me

Получить информацию о текущем боте.

```python
me = await bot.get_me()
print(me.username)
```

## get_updates

Низкоуровневое получение обновлений (если вы не используете `start_polling`).

```python
resp = await bot.get_updates(limit=100, timeout=30)
for raw_update in resp.get("updates", []):
    # при необходимости вручную передаём в диспетчер
    await bot.dispatcher.dispatch(raw_update)
```

## start_polling

Запуск long polling с автоматической диспетчеризацией.

```python
await bot.start_polling(
    limit=100,
    timeout=30,
    types=["message_created", "message_callback"]
)
```

## See Also

- [Messages](messages.md) - методы сообщений
- [Webhooks](webhooks.md) - методы webhook-подписок
