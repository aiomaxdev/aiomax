# Webhooks

В aiomax webhook управляется двумя слоями:
1) HTTP-сервер (`start_webhook` / `stop_webhook`),
2) подписки в MAX API (`set_subscription` / `get_subscriptions` / `delete_subscription`).

## start_webhook

Поднимает локальный aiohttp-сервер для приёма обновлений.

```python
await bot.start_webhook(
    host="0.0.0.0",
    port=8080,
    path="/webhook",
    webhook_url="https://example.com/webhook",
    secret="super-secret"
)
```

Если передан `webhook_url`, метод дополнительно вызывает `set_subscription(...)`.

## stop_webhook

Останавливает локальный webhook-сервер.

```python
await bot.stop_webhook()
```

## set_subscription

Создать подписку в MAX API.

```python
await bot.set_subscription(
    url="https://example.com/webhook",
    update_types=["message_created", "message_callback"],
    secret="super-secret"
)
```

## get_subscriptions

Получить список активных подписок.

```python
subs = await bot.get_subscriptions()
print(subs.subscriptions)
```

## delete_subscription

Удалить подписку по URL.

```python
await bot.delete_subscription(url="https://example.com/webhook")
```

## See Also

- [Webhook Guide](../guides/webhook.md)
- [Polling](../guides/polling.md)
