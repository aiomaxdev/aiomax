--- docs/guides/middleware.md (原始)


+++ docs/guides/middleware.md (修改后)
# Middleware

Middleware allows you to preprocess or postprocess updates before they reach handlers.

## Basic Middleware

```python
from aiomax import Bot, BaseMiddleware

bot = Bot(token="YOUR_TOKEN")

class LoggingMiddleware(BaseMiddleware):
    async def pre_process(self, update):
        print(f"Received update: {update.update_id}")

    async def post_process(self, update, exception=None):
        if exception:
            print(f"Error processing update: {exception}")

bot.use_middleware(LoggingMiddleware())
```

## Use Cases

### Authentication

```python
class AuthMiddleware(BaseMiddleware):
    async def pre_process(self, update):
        if not await self.is_authorized(update):
            raise PermissionError("Unauthorized")

    async def is_authorized(self, update):
        # Check user permissions
        return True
```

### Rate Limiting

```python
from collections import defaultdict
import time

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, rate=10, period=60):
        self.requests = defaultdict(list)
        self.rate = rate
        self.period = period

    async def pre_process(self, update):
        user_id = update.message.from_user.id
        now = time.time()

        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < self.period
        ]

        if len(self.requests[user_id]) >= self.rate:
            raise Exception("Rate limit exceeded")

        self.requests[user_id].append(now)
```

### Database Session

```python
class DBSessionMiddleware(BaseMiddleware):
    async def pre_process(self, update):
        update.db_session = await db.create_session()

    async def post_process(self, update, exception=None):
        await update.db_session.close()
```

## Middleware Order

Middleware is executed in registration order for `pre_process` and reverse order for `post_process`.

```python
bot.use_middleware(LoggingMiddleware())   # 1st pre, 3rd post
bot.use_middleware(AuthMiddleware())      # 2nd pre, 2nd post
bot.use_middleware(RateLimitMiddleware()) # 3rd pre, 1st post
```

## See Also

- [Handlers](handlers.md) - Working with handlers