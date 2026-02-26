import asyncio
from typing import Callable, Coroutine, Any, Dict, List
from aiomax.types.update import Update

Handler = Callable[[Update], Coroutine[Any, Any, None]]


class Dispatcher:
    def __init__(self):
        self._handlers: Dict[str, List[Handler]] = {}

    # Декоратор для сообщений
    def message(self) -> Callable[[Handler], Handler]:
        return self._register("message_created")

    def _register(self, update_type: str) -> Callable[[Handler], Handler]:
        def decorator(func: Handler) -> Handler:
            self._handlers.setdefault(update_type, []).append(func)
            return func
        return decorator

    async def dispatch(self, update: Update):
        handlers = self._handlers.get(update.update_type, [])
        for handler in handlers:
            await handler(update)

    async def polling(
        self,
        bot,
        poll_interval: float = 3.0,
        stop_event: asyncio.Event | None = None
    ):
        """Long polling с использованием bot.get_updates()"""
        stop_event = stop_event or asyncio.Event()
        offset: int | None = None
        while not stop_event.is_set():
            try:
                updates = await bot.get_updates(offset=offset)
                for update in updates:
                    # Для следующего запроса передаем timestamp + 1
                    offset = update.timestamp + 1
                    await self.dispatch(update)
            except Exception as e:
                print(f"[Dispatcher] Ошибка: {e}")
            await asyncio.sleep(poll_interval)

    async def run_polling(self, bot, poll_interval: float = 3.0):
        await self.polling(bot, poll_interval=poll_interval)