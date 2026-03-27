"""
aiomax/dispatcher.py

Диспетчер - центральный компонент для управления обработкой событий.
Координирует работу роутеров, middleware и хранилища состояний.
"""
import asyncio
from typing import Dict, List, Any, Optional, Callable
from .router import Router


class Middleware:
    """Базовый класс для middleware."""
    
    async def __call__(self, event: Dict[str, Any], call_next: Callable):
        raise NotImplementedError


class ErrorMiddleware(Middleware):
    """Middleware для обработки ошибок."""
    
    def __init__(self, error_handler: Callable):
        self.error_handler = error_handler
    
    async def __call__(self, event: Dict[str, Any], call_next: Callable):
        try:
            return await call_next(event)
        except Exception as e:
            await self.error_handler(e, event)


class Dispatcher:
    """
    Диспетчер событий.
    Аналог Dispatcher в aiogram - управляет обработкой всех входящих событий.
    """
    
    def __init__(self, storage: Optional[Any] = None):
        self.storage = storage
        self._root_router = Router("root")
        self._middleware: List[Middleware] = []
        self._error_handlers: List[Callable] = []
    
    @property
    def router(self) -> Router:
        """Возвращает корневой роутер для регистрации обработчиков."""
        return self._root_router
    
    def include_router(self, router: Router):
        """Подключение роутера к диспетчеру."""
        self._root_router.include_router(router)
    
    def register_middleware(self, middleware: Middleware):
        """Регистрация middleware."""
        self._middleware.append(middleware)
    
    def errors(self):
        """Декоратор для регистрации обработчика ошибок."""
        def decorator(func: Callable):
            self._error_handlers.append(func)
            self.register_middleware(ErrorMiddleware(func))
            return func
        return decorator
    
    async def _run_middleware_chain(
        self, 
        event: Dict[str, Any], 
        middleware_index: int = 0
    ):
        """Рекурсивный запуск цепочки middleware."""
        if middleware_index >= len(self._middleware):
            # Все middleware пройдены, обрабатываем событие
            event_type = self._get_event_type(event)
            return await self._root_router.process_event(event_type, event)
        
        middleware = self._middleware[middleware_index]
        
        async def call_next(evt):
            return await self._run_middleware_chain(evt, middleware_index + 1)
        
        return await middleware(event, call_next)
    
    def _get_event_type(self, event: Dict[str, Any]) -> str:
        """Определение типа события из объекта Update."""
        # Примерная логика определения типа события
        if "message" in event:
            return "message_created"
        elif "callback_query" in event:
            return "callback_query"
        elif "bot_started" in event:
            return "bot_started"
        elif "message_removed" in event:
            return "message_removed"
        else:
            return "unknown"
    
    async def feed_update(self, update: Dict[str, Any]) -> bool:
        """
        Передача обновления в диспетчер для обработки.
        Возвращает True, если обновление было обработано.
        """
        return await self._run_middleware_chain(update)
    
    async def start_polling(self, bot: Any, **kwargs):
        """
        Запуск поллинга событий через бота.
        """
        print("Starting polling...")
        async for updates in bot.start_polling(**kwargs):
            if isinstance(updates, list):
                for update in updates:
                    await self.feed_update(update)
            else:
                await self.feed_update(updates)
    
    async def start_webhook(self, app: Any, bot: Any, path: str = "/webhook"):
        """
        Настройка вебхука для получения событий.
        Требует передачи настроенного web-приложения (например, aiohttp).
        """
        from aiohttp import web
        
        async def webhook_handler(request):
            # Проверка секретного ключа если есть
            secret = request.headers.get("X-Max-Bot-Api-Secret")
            expected_secret = getattr(bot, "webhook_secret", None)
            
            if expected_secret and secret != expected_secret:
                return web.Response(status=403, text="Forbidden")
            
            try:
                update = await request.json()
                await self.feed_update(update)
                return web.Response(status=200, text="OK")
            except Exception as e:
                print(f"Error processing webhook: {e}")
                return web.Response(status=500, text="Internal Server Error")
        
        app.router.add_post(path, webhook_handler)
        return app
