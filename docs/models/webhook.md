--- docs/models/webhook.md (原始)


+++ docs/models/webhook.md (修改后)
# WebhookInfo

Contains information about the current webhook status.

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `url` | `str` | Webhook URL |
| `has_custom_certificate` | `bool` | True if using custom certificate |
| `pending_update_count` | `int` | Number of pending updates |
| `ip_address` | `str` | IP address used for webhook |
| `last_error_date` | `datetime` | Date of last error (if any) |
| `last_error_message` | `str` | Error message (if any) |
| `max_connections` | `int` | Maximum allowed connections |
| `allowed_updates` | `list` | List of allowed update types |

## Getting Webhook Info

```python
info = await bot.get_webhook_info()

print(f"URL: {info.url}")
print(f"Pending: {info.pending_update_count}")
print(f"Max connections: {info.max_connections}")

if info.last_error_message:
    print(f"Last error: {info.last_error_message}")
```

## Checking Webhook Status

```python
info = await bot.get_webhook_info()

if info.url:
    print("Webhook is active")
else:
    print("Webhook is not set")
```

## Setting Webhook with Options

```python
await bot.set_webhook(
    url="https://example.com/webhook",
    max_connections=100,
    allowed_updates=["message", "callback_query"]
)

info = await bot.get_webhook_info()
print(info.allowed_updates)  # ["message", "callback_query"]
```

## See Also

- [Webhook Guide](../guides/webhook.md) - Webhook configuration
- [API Methods](../methods/webhooks.md) - Webhook API methods