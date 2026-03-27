"""
aiomax/router.py

Реализация системы роутинга (диспетчеризации) событий, похожей на aiogram.
Позволяет регистрировать обработчики с фильтрами и автоматически вызывать их при получении событий.
"""
from typing import Callable, Dict, List, Any, Optional, Union
from enum import Enum


class Filter:
    """Базовый класс для фильтров событий."""
    
    async def __call__(self, event: Dict[str, Any]) -> bool:
        raise NotImplementedError


class TextFilter(Filter):
    """Фильтр по тексту сообщения."""
    
    def __init__(self, text: Union[str, List[str]]):
        self.texts = [text] if isinstance(text, str) else text
    
    async def __call__(self, event: Dict[str, Any]) -> bool:
        message = event.get("message", {})
        content = message.get("content", "")
        return content in self.texts


class CommandFilter(Filter):
    """Фильтр по командам (например, /start, /help)."""
    
    def __init__(self, commands: Union[str, List[str]], prefix: str = "/"):
        self.commands = [commands] if isinstance(commands, str) else commands
        self.prefix = prefix
    
    async def __call__(self, event: Dict[str, Any]) -> bool:
        message = event.get("message", {})
        content = message.get("content", "")
        
        if not content.startswith(self.prefix):
            return False
        
        command = content.split()[0][len(self.prefix):]
        return command in self.commands


class CallbackDataFilter(Filter):
    """Фильтр для коллбэк-данных (если поддерживается платформой)."""
    
    def __init__(self, data: Union[str, List[str]]):
        self.data = [data] if isinstance(data, str) else data
    
    async def __call__(self, event: Dict[str, Any]) -> bool:
        # Предполагаемая структура для коллбэков
        callback = event.get("callback_query", {})
        callback_data = callback.get("data", "")
        return callback_data in self.data


class Router:
    """
    Роутер для группировки обработчиков событий.
    Позволяет создавать модульную структуру бота.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self._handlers: Dict[str, List[Dict[str, Any]]] = {}
        self._parent_routers: List["Router"] = []
    
    def register_handler(
        self,
        event_type: str,
        handler: Callable,
        filters: Optional[List[Filter]] = None
    ):
        """Регистрация обработчика события."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        self._handlers[event_type].append({
            "handler": handler,
            "filters": filters or []
        })
    
    def message(self, *filters: Filter):
        """Декоратор для регистрации обработчика сообщений."""
        def decorator(func: Callable):
            self.register_handler("message_created", func, list(filters))
            return func
        return decorator
    
    def command(self, *commands: str, prefix: str = "/"):
        """Декоратор для регистрации обработчика команд."""
        def decorator(func: Callable):
            cmd_filter = CommandFilter(list(commands), prefix)
            self.register_handler("message_created", func, [cmd_filter])
            return func
        return decorator
    
    def callback_query(self, *data: str):
        """Декоратор для регистрации обработчика коллбэк-запросов."""
        def decorator(func: Callable):
            cb_filter = CallbackDataFilter(list(data))
            self.register_handler("callback_query", func, [cb_filter])
            return func
        return decorator
    
    def include_router(self, router: "Router"):
        """Подключение другого роутера к текущему."""
        self._parent_routers.append(router)
    
    async def process_event(self, event_type: str, event: Dict[str, Any]) -> bool:
        """
        Обработка события. Возвращает True, если событие было обработано.
        """
        # Сначала проверяем собственные обработчики
        handlers = self._handlers.get(event_type, [])
        
        for handler_info in handlers:
            handler = handler_info["handler"]
            filters = handler_info["filters"]
            
            # Проверка всех фильтров
            passed = True
            for f in filters:
                if not await f(event):
                    passed = False
                    break
            
            if passed:
                try:
                    await handler(event)
                    return True
                except Exception as e:
                    print(f"Error in handler {handler.__name__}: {e}")
                    continue
        
        # Если не обработано, проверяем подключенные роутеры
        for router in self._parent_routers:
            if await router.process_event(event_type, event):
                return True
        
        return False
    
    def get_all_handlers(self) -> Dict[str, List[Dict[str, Any]]]:
        """Получение всех обработчиков включая подключенные роутеры."""
        all_handlers = dict(self._handlers)
        
        for router in self._parent_routers:
            router_handlers = router.get_all_handlers()
            for event_type, handlers in router_handlers.items():
                if event_type not in all_handlers:
                    all_handlers[event_type] = []
                all_handlers[event_type].extend(handlers)
        
        return all_handlers
