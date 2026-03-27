from typing import Callable, Awaitable, Dict, Any, List, Optional
from aiomax.models.update import Update
from aiomax.enums.update_type import UpdateTypeEnum


class Handler:
    """Базовый класс для обработчиков"""

    def __init__(self, callback: Callable[[Update], Awaitable[Any]]):
        self.callback = callback

    async def call(self, update: Update) -> Any:
        return await self.callback(update)


class Dispatcher:
    """Диспетчер для обработки обновлений"""

    def __init__(self):
        self._handlers: Dict[UpdateTypeEnum, List[Handler]] = {}
        self._default_handler: Optional[Handler] = None

    def register_handler(
        self,
        update_type: UpdateTypeEnum | str,
        callback: Callable[[Update], Awaitable[Any]]
    ) -> Handler:
        """Регистрация обработчика для конкретного типа обновления"""
        if isinstance(update_type, str):
            update_type = UpdateTypeEnum(update_type)

        handler = Handler(callback)

        if update_type not in self._handlers:
            self._handlers[update_type] = []

        self._handlers[update_type].append(handler)
        return handler

    def register_default_handler(
        self,
        callback: Callable[[Update], Awaitable[Any]]
    ) -> Handler:
        """Регистрация обработчика по умолчанию (для всех типов)"""
        handler = Handler(callback)
        self._default_handler = handler
        return handler

    def on_message(self, callback: Callable[[Update], Awaitable[Any]]) -> Handler:
        """Декоратор для регистрации обработчика сообщений"""
        return self.register_handler(UpdateTypeEnum.MESSAGE_CREATED, callback)

    def on_callback(self, callback: Callable[[Update], Awaitable[Any]]) -> Handler:
        """Декоратор для регистрации обработчика callback"""
        return self.register_handler(UpdateTypeEnum.MESSAGE_CALLBACK, callback)

    def on_bot_started(self, callback: Callable[[Update], Awaitable[Any]]) -> Handler:
        """Декоратор для регистрации обработчика старта бота"""
        return self.register_handler(UpdateTypeEnum.BOT_STARTED, callback)

    def on_message_edited(self, callback: Callable[[Update], Awaitable[Any]]) -> Handler:
        """Декоратор для регистрации обработчика редактирования сообщения"""
        return self.register_handler(UpdateTypeEnum.MESSAGE_EDITED, callback)

    def on_message_removed(self, callback: Callable[[Update], Awaitable[Any]]) -> Handler:
        """Декоратор для регистрации обработчика удаления сообщения"""
        return self.register_handler(UpdateTypeEnum.MESSAGE_REMOVED, callback)

    async def process_update(self, update: Update) -> List[Any]:
        """Обработка обновления"""
        results = []

        # Получаем handlers для конкретного типа
        handlers = self._handlers.get(update.type, [])

        # Вызываем все зарегистрированные handlers
        for handler in handlers:
            try:
                result = await handler.call(update)
                results.append(result)
            except Exception as e:
                # Логируем ошибку но продолжаем обработку
                print(f"Error in handler for {update.type}: {e}")

        # Вызываем default handler если есть
        if self._default_handler:
            try:
                result = await self._default_handler.call(update)
                results.append(result)
            except Exception as e:
                print(f"Error in default handler: {e}")

        return results

    async def dispatch(self, update_ Dict[str, Any]) -> List[Any]:
        """Преобразование сырых данных в Update и обработка"""
        update = Update.from_dict(update_data)
        return await self.process_update(update)


__all__ = ["Handler", "Dispatcher"]