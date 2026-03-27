from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union
from enum import Enum


class EventType(str, Enum):
    """Типы событий для фильтрации"""
    MESSAGE = "message_created"
    CALLBACK = "message_callback"
    MESSAGE_EDITED = "message_edited"
    MESSAGE_REMOVED = "message_removed"
    BOT_STARTED = "bot_started"
    USER_ADDED = "user_added"
    USER_REMOVED = "user_removed"
    CHAT_TITLE_CHANGED = "chat_title_changed"


class BaseFilter(ABC):
    """Базовый класс для фильтров"""
    
    @abstractmethod
    async def __call__(self, event: Dict[str, Any]) -> bool:
        """Проверка события"""
        pass


class Filter(BaseFilter):
    """Простой фильтр на основе callable"""
    
    def __init__(self, func: Callable[[Dict[str, Any]], Awaitable[bool]]):
        self.func = func
    
    async def __call__(self, event: Dict[str, Any]) -> bool:
        return await self.func(event)


class Handler(ABC):
    """Базовый класс обработчика"""
    
    def __init__(self, callback: Callable, filters: Optional[List[BaseFilter]] = None):
        self.callback = callback
        self.filters = filters or []
    
    async def check(self, event: Dict[str, Any]) -> bool:
        """Проверка всех фильтров"""
        for filter_ in self.filters:
            if not await filter_(event):
                return False
        return True
    
    @abstractmethod
    async def handle(self, event: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Обработка события"""
        pass


class MessageHandler(Handler):
    """Обработчик сообщений"""
    
    async def handle(self, event: Dict[str, Any], context: Dict[str, Any]) -> Any:
        return await self.callback(event, context)


class CallbackHandler(Handler):
    """Обработчик callback-запросов"""
    
    async def handle(self, event: Dict[str, Any], context: Dict[str, Any]) -> Any:
        return await self.callback(event, context)


class State:
    """Класс состояния для FSM"""
    
    def __init__(self, name: str = ""):
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other) -> bool:
        if isinstance(other, State):
            return self.name == other.name
        return self.name == other


class StatesGroup:
    """Базовый класс для групп состояний FSM"""
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Автоматически создаём состояния из атрибутов класса
        for attr_name, attr_value in list(cls.__dict__.items()):
            if isinstance(attr_value, State):
                if not attr_value.name:
                    attr_value.name = f"{cls.__name__}:{attr_name}"
