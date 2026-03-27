from abc import ABC
from typing import Any, Awaitable, Callable, Dict, List, Optional


class Middleware(ABC):
    """
    Базовый класс для middleware.
    Аналог middleware в aiogram.
    
    Middleware позволяют выполнять код до и после обработки события.
    Примеры использования:
    - Логирование
    - Аутентификация
    - Ограничение доступа (rate limiting)
    - Модификация контекста
    """
    
    async def __call__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
        call_next: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Any:
        """
        Вызов middleware.
        
        Args:
            event: Событие для обработки
            context: Контекст выполнения
            call_next: Функция для вызова следующего middleware или обработчика
        
        Returns:
            Результат обработки
        """
        return await call_next(event, context)


class SimpleMiddleware(Middleware):
    """Простой middleware на основе callable"""
    
    def __init__(self, func: Callable):
        self.func = func
    
    async def __call__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
        call_next: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Any:
        return await self.func(event, context, call_next)


class LoggingMiddleware(Middleware):
    """Middleware для логирования событий"""
    
    def __init__(self, logger=None):
        self.logger = logger or print
    
    async def __call__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
        call_next: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Any:
        event_type = event.get("type", "unknown")
        self.logger(f"[Middleware] Получено событие типа: {event_type}")
        
        result = await call_next(event, context)
        
        self.logger(f"[Middleware] Событие обработано")
        return result


class RateLimitMiddleware(Middleware):
    """
    Middleware для ограничения частоты запросов.
    Простая реализация для примера.
    """
    
    def __init__(self, rate: int = 10, window: int = 60):
        self.rate = rate  # Максимальное количество запросов
        self.window = window  # Окно времени в секундах
        self._requests: Dict[int, List[float]] = {}
    
    async def __call__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
        call_next: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Any:
        import time
        
        user_id = event.get("message", {}).get("sender", {}).get("user_id")
        if not user_id:
            return await call_next(event, context)
        
        now = time.time()
        
        if user_id not in self._requests:
            self._requests[user_id] = []
        
        # Очищаем старые запросы
        self._requests[user_id] = [
            ts for ts in self._requests[user_id]
            if now - ts < self.window
        ]
        
        if len(self._requests[user_id]) >= self.rate:
            self.logger(f"[RateLimit] Пользователь {user_id} превысил лимит")
            return None  # Или выбросить исключение
        
        self._requests[user_id].append(now)
        return await call_next(event, context)


class ContextMiddleware(Middleware):
    """Middleware для добавления данных в контекст"""
    
    def __init__(self, data_getter: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.data_getter = data_getter
    
    async def __call__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
        call_next: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Any:
        extra_data = self.data_getter(event)
        context.update(extra_data)
        return await call_next(event, context)
