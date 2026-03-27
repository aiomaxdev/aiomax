from typing import Any, Awaitable, Callable, Dict, List, Optional
from aiomax.handlers.handler import Handler, BaseFilter, EventType, MessageHandler


class Router:
    """
    Роутер для регистрации обработчиков событий.
    Аналог Dispatcher в aiogram.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self._handlers: Dict[EventType, List[Handler]] = {event_type: [] for event_type in EventType}
        self._filters: List[BaseFilter] = []
        self._parent: Optional["Router"] = None
        self._children: List["Router"] = []
    
    def add_filter(self, filter_: BaseFilter) -> None:
        """Добавить глобальный фильтр для всех обработчиков роутера"""
        self._filters.append(filter_)
    
    def include_router(self, router: "Router") -> None:
        """Подключить другой роутер к текущему"""
        router._parent = self
        self._children.append(router)
    
    def _get_all_handlers(self) -> Dict[EventType, List[Handler]]:
        """Получить все обработчики включая дочерние роутеры"""
        all_handlers: Dict[EventType, List[Handler]] = {event_type: [] for event_type in EventType}
        
        # Добавляем обработчики текущего роутера
        for event_type, handlers in self._handlers.items():
            all_handlers[event_type].extend(handlers)
        
        # Добавляем обработчики дочерних роутеров
        for child in self._children:
            child_handlers = child._get_all_handlers()
            for event_type, handlers in child_handlers.items():
                all_handlers[event_type].extend(handlers)
        
        return all_handlers
    
    async def process_event(self, event: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Обработать событие.
        Возвращает True, если событие было обработано, иначе False.
        """
        event_type_str = event.get("type", "")
        
        # Пытаемся найти соответствующий EventType
        try:
            event_type = EventType(event_type_str)
        except ValueError:
            return False
        
        all_handlers = self._get_all_handlers()
        handlers = all_handlers.get(event_type, [])
        
        for handler in handlers:
            # Проверяем глобальные фильтры роутера
            for filter_ in self._filters:
                if not await filter_(event):
                    continue
            
            # Проверяем фильтры обработчика
            if await handler.check(event):
                await handler.handle(event, context)
                return True
        
        return False
    
    def register_handler(
        self,
        event_type: EventType,
        *filters: BaseFilter,
    ) -> Callable[[Callable], Callable]:
        """
        Декоратор для регистрации обработчика.
        
        Пример использования:
            @router.on_message()
            async def handle_message(event, context):
                ...
            
            @router.on_message(F.Text("hello"))
            async def handle_hello(event, context):
                ...
        """
        def decorator(callback: Callable) -> Callable:
            handler = MessageHandler(callback, filters=list(filters))
            self._handlers[event_type].append(handler)
            return callback
        return decorator
    
    def on_message(self, *filters: BaseFilter) -> Callable[[Callable], Callable]:
        """Регистрация обработчика сообщений"""
        return self.register_handler(EventType.MESSAGE, *filters)
    
    def on_callback(self, *filters: BaseFilter) -> Callable[[Callable], Callable]:
        """Регистрация обработчика callback-запросов"""
        return self.register_handler(EventType.CALLBACK, *filters)
    
    def on_edited_message(self, *filters: BaseFilter) -> Callable[[Callable], Callable]:
        """Регистрация обработчика редактированных сообщений"""
        return self.register_handler(EventType.MESSAGE_EDITED, *filters)
    
    def on_bot_started(self, *filters: BaseFilter) -> Callable[[Callable], Callable]:
        """Регистрация обработчика запуска бота"""
        return self.register_handler(EventType.BOT_STARTED, *filters)
