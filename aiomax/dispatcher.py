"""
Диспетчер для обработки обновлений.

"""
import asyncio
from typing import Callable, Awaitable, Dict, Any, List, Optional, Union
from aiomax.models.update import Update
from aiomax.enums.update_type import UpdateTypeEnum
from aiomax.filters import BaseFilter


class Handler:
    """Класс для представления обработчика с фильтрами"""

    def __init__(
        self,
        callback: Callable[[Update], Awaitable[Any]],
        filters: Optional[List[BaseFilter]] = None
    ):
        self.callback = callback
        self.filters = filters or []

    async def check(self, update: Update) -> bool:
        """Проверка фильтров"""
        for filter in self.filters:
            if not await filter.check(update):
                return False
        return True

    async def call(self, update: Update) -> Any:
        """Вызов обработчика"""
        return await self.callback(update)


class Dispatcher:
    """Диспетчер для обработки обновлений"""

    def __init__(self):
        self._handlers: Dict[UpdateTypeEnum, List[Handler]] = {}
        self._default_handler: Optional[Handler] = None

    def register_handler(
        self,
        update_type: Union[UpdateTypeEnum, str],
        callback: Callable[[Update], Awaitable[Any]],
        filters: Optional[List[BaseFilter]] = None
    ) -> Handler:
        """
        Регистрация обработчика для конкретного типа обновления.

        Args:
            update_type: Тип обновления (enum или строка)
            callback: Функция обработчика
            filters: Список фильтров для обработки

        Returns:
            Созданный Handler
        """
        if isinstance(update_type, str):
            update_type = UpdateTypeEnum(update_type)

        handler = Handler(callback, filters)

        if update_type not in self._handlers:
            self._handlers[update_type] = []

        self._handlers[update_type].append(handler)
        return handler

    def register_default_handler(
        self,
        callback: Callable[[Update], Awaitable[Any]],
        filters: Optional[List[BaseFilter]] = None
    ) -> Handler:
        """Регистрация обработчика по умолчанию (для всех типов)"""
        handler = Handler(callback, filters)
        self._default_handler = handler
        return handler

    def on_message(
        self,
        *filters: BaseFilter
    ) -> Callable[[Callable[[Update], Awaitable[Any]]], Handler]:
        """
        Декоратор для регистрации обработчика сообщений.

        Args:
            *filters: Фильтры для применения к обработчику

        Example:
            @dispatcher.on_message(F.text.contains('привет'))
            async def handle_hello(update):
                ...
        """
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Handler:
            return self.register_handler(
                UpdateTypeEnum.MESSAGE_CREATED,
                callback,
                list(filters)
            )
        return decorator

    def on_callback(
        self,
        *filters: BaseFilter
    ) -> Callable[[Callable[[Update], Awaitable[Any]]], Handler]:
        """Декоратор для регистрации обработчика callback"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Handler:
            return self.register_handler(
                UpdateTypeEnum.MESSAGE_CALLBACK,
                callback,
                list(filters)
            )
        return decorator

    def on_bot_started(
        self,
        *filters: BaseFilter
    ) -> Callable[[Callable[[Update], Awaitable[Any]]], Handler]:
        """Декоратор для регистрации обработчика старта бота"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Handler:
            return self.register_handler(
                UpdateTypeEnum.BOT_STARTED,
                callback,
                list(filters)
            )
        return decorator

    def on_message_edited(
        self,
        *filters: BaseFilter
    ) -> Callable[[Callable[[Update], Awaitable[Any]]], Handler]:
        """Декоратор для регистрации обработчика редактирования сообщения"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Handler:
            return self.register_handler(
                UpdateTypeEnum.MESSAGE_EDITED,
                callback,
                list(filters)
            )
        return decorator

    def on_message_removed(
        self,
        *filters: BaseFilter
    ) -> Callable[[Callable[[Update], Awaitable[Any]]], Handler]:
        """Декоратор для регистрации обработчика удаления сообщения"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Handler:
            return self.register_handler(
                UpdateTypeEnum.MESSAGE_REMOVED,
                callback,
                list(filters)
            )
        return decorator

    async def process_update(self, update: Update) -> List[Any]:
        handlers = self._handlers.get(update.type, [])

        async def run(handler):
            try:
                if await handler.check(update):
                    return await handler.call(update)
            except Exception:
                import traceback
                traceback.print_exc()

        tasks = [run(handler) for handler in handlers]

        if self._default_handler:
            tasks.append(run(self._default_handler))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return [r for r in results if r is not None]
    
    async def dispatch(self, update_data: Dict[str, Any]) -> List[Any]:
        """Преобразование сырых данных в Update и обработка"""
        print("UPDATE:", update_data)
        update = Update.from_dict(update_data)
        return await self.process_update(update)


__all__ = ["Handler", "Dispatcher"]