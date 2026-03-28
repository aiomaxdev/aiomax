# Webhook

В aiomax webhook состоит из:
- локального HTTP-сервера (`start_webhook`),
- подписки в MAX API (`set_subscription`).

## Быстрый старт

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

async def main():
    await bot.start()

    await bot.start_webhook(
        host="0.0.0.0",
        port=8080,
        path="/webhook",
        webhook_url="https://your-domain.com/webhook",
        secret="my-secret"
    )

    # приложение продолжает работать, пока процесс жив
```

## Управление подписками

```python
await bot.set_subscription(
    url="https://your-domain.com/webhook",
    update_types=["message_created", "message_callback"],
    secret="my-secret"
)

subs = await bot.get_subscriptions()
await bot.delete_subscription(url="https://your-domain.com/webhook")
```

## Остановка webhook сервера

```python
await bot.stop_webhook()
await bot.close()
```
