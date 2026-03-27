# Webhooks

Methods for managing webhooks.

## set_webhook

Set up a webhook for receiving updates.

```python
await bot.set_webhook(
    url="https://your-domain.com/webhook",
    certificate=None,           # Optional: path to cert file
    ip_address=None,            # Optional: static IP
    max_connections=40,         # Max concurrent connections
    allowed_updates=[           # List of update types to receive
        "message",
        "callback_query",
        "chat_member"
    ],
    drop_pending_updates=False, # Drop pending updates on start
    secret_token=None           # Secret token for verification
)
```

## With Custom Certificate

```python
await bot.set_webhook(
    url="https://your-domain.com/webhook",
    certificate="/path/to/cert.pem",
    max_connections=100
)
```

## delete_webhook

Remove the webhook.

```python
await bot.delete_webhook(drop_pending_updates=True)
```

## get_webhook_info

Get current webhook information.

```python
info = await bot.get_webhook_info()

print(f"URL: {info.url}")
print(f"Pending updates: {info.pending_update_count}")
print(f"Max connections: {info.max_connections}")
print(f"Allowed updates: {info.allowed_updates}")

if info.last_error_message:
    print(f"Last error: {info.last_error_message}")
    print(f"Error date: {info.last_error_date}")
```

## Checking Webhook Status

```python
info = await bot.get_webhook_info()

if info.url:
    print("✅ Webhook is active")
    print(f"   URL: {info.url}")
else:
    print("❌ No webhook configured")
```

## Handling Pending Updates

```python
info = await bot.get_webhook_info()

if info.pending_update_count > 0:
    print(f"Processing {info.pending_update_count} pending updates...")
```

## Complete Setup Example

```python
from aiohttp import web
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")
app = web.Application()

async def webhook_handler(request):
    update = await request.json()

    # Verify secret token if configured
    secret = request.headers.get('X-MAX-Token')
    if secret != SECRET_TOKEN:
        return web.Response(status=403)

    await bot.process_update(update)
    return web.Response()

app.router.add_post('/webhook', webhook_handler)

async def setup():
    # Set webhook
    await bot.set_webhook(
        url="https://your-domain.com/webhook",
        secret_token=SECRET_TOKEN,
        max_connections=100
    )

    # Start server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

async def shutdown():
    await bot.delete_webhook()

asyncio.run(setup())
```

## Switching from Polling to Webhook

```python
# First, stop polling and delete any existing webhook
await bot.delete_webhook(drop_pending_updates=False)

# Then set up new webhook
await bot.set_webhook(
    url="https://your-new-domain.com/webhook",
    drop_pending_updates=True
)
```

## See Also

- [Webhook Guide](../guides/webhook.md) - Webhook configuration guide
- [Polling](../guides/polling.md) - Alternative long polling method