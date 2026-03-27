# Webhook

Webhooks allow MAX to push updates to your server in real-time.

## Basic Setup

```python
from aiomax import Bot
from aiohttp import web

bot = Bot(token="YOUR_TOKEN")
app = web.Application()

async def webhook_handler(request):
    update = await request.json()
    await bot.process_update(update)
    return web.Response()

app.router.add_post('/webhook', webhook_handler)
```

## Setting Webhook

```python
await bot.set_webhook(
    url="https://your-domain.com/webhook",
    certificate="/path/to/cert.pem",  # Optional
    ip_address="192.168.1.1"          # Optional
)
```

## Removing Webhook

```python
await bot.delete_webhook()
```

## Getting Webhook Info

```python
info = await bot.get_webhook_info()
print(f"URL: {info.url}")
print(f"Pending updates: {info.pending_update_count}")
```

## Running with aiohttp

```python
async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    await bot.start_webhook(path='/webhook')

asyncio.run(main())
```

## See Also

- [Polling](polling.md) - Alternative update method