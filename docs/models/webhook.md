# Webhook Models

Для webhook-подписок используются модели:

- `SubscriptionsResponse`
- `SubscriptionResponse`

Пример:

```python
subs = await bot.get_subscriptions()
created = await bot.set_subscription(url="https://example.com/webhook")
removed = await bot.delete_subscription(url="https://example.com/webhook")
```
