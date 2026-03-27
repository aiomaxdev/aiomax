"""
Система фильтров для обработки обновлений.

Фильтры позволяют гибко настраивать условия, при которых
обработчики будут вызываться.
"""
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Optional, Union
from aiomax.models.update import Update


class BaseFilter(ABC):
    """Базовый класс для всех фильтров"""

    @abstractmethod
    async def check(self, update: Update) -> bool:
        """
        Проверка обновления.

        Args:
            update: Обновление для проверки

        Returns:
            True если обновление проходит фильтр, False иначе
        """
        pass

    def __and__(self, other: "BaseFilter") -> "AndFilter":
        """Логическое И для фильтров"""
        return AndFilter(self, other)

    def __or__(self, other: "BaseFilter") -> "OrFilter":
        """Логическое ИЛИ для фильтров"""
        return OrFilter(self, other)

    def __invert__(self) -> "NotFilter":
        """Логическое НЕ для фильтра"""
        return NotFilter(self)


class AndFilter(BaseFilter):
    """Фильтр, объединяющий несколько фильтров через И"""

    def __init__(self, *filters: BaseFilter):
        self.filters = filters

    async def check(self, update: Update) -> bool:
        for filter in self.filters:
            if not await filter.check(update):
                return False
        return True


class OrFilter(BaseFilter):
    """Фильтр, объединяющий несколько фильтров через ИЛИ"""

    def __init__(self, *filters: BaseFilter):
        self.filters = filters

    async def check(self, update: Update) -> bool:
        for filter in self.filters:
            if await filter.check(update):
                return True
        return False


class NotFilter(BaseFilter):
    """Инвертирующий фильтр"""

    def __init__(self, filter: BaseFilter):
        self.filter = filter

    async def check(self, update: Update) -> bool:
        return not await self.filter.check(update)


class TextFilter(BaseFilter):
    """Фильтр для проверки текста сообщения"""

    def __init__(
        self,
        text: Optional[str] = None,
        contains: Optional[str] = None,
        startswith: Optional[str] = None,
        endswith: Optional[str] = None,
        regex: Optional[str] = None,
    ):
        self.text = text
        self.contains = contains
        self.startswith = startswith
        self.endswith = endswith
        self.regex = regex

    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.body:
            return False

        message_text = update.message.body.text
        if not message_text:
            return False

        if self.text is not None and message_text != self.text:
            return False

        if self.contains is not None and self.contains not in message_text:
            return False

        if self.startswith is not None and not message_text.startswith(self.startswith):
            return False

        if self.endswith is not None and not message_text.endswith(self.endswith):
            return False

        if self.regex is not None:
            import re
            if not re.search(self.regex, message_text):
                return False

        return True


class ChatIDFilter(BaseFilter):
    """Фильтр по ID чата"""

    def __init__(self, chat_id: Union[int, list[int]]):
        if isinstance(chat_id, int):
            self.chat_ids = [chat_id]
        else:
            self.chat_ids = chat_id

    async def check(self, update: Update) -> bool:
        return update.chat_id in self.chat_ids


class UserIDFilter(BaseFilter):
    """Фильтр по ID пользователя"""

    def __init__(self, user_id: Union[int, list[int]]):
        if isinstance(user_id, int):
            self.user_ids = [user_id]
        else:
            self.user_ids = user_id

    async def check(self, update: Update) -> bool:
        return update.user_id in self.user_ids


class CommandFilter(BaseFilter):
    """Фильтр для команд (сообщения, начинающиеся с /)"""

    def __init__(self, command: str, prefix: str = "/"):
        self.command = command
        self.prefix = prefix

    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.body:
            return False

        message_text = update.message.body.text
        if not message_text:
            return False

        if not message_text.startswith(self.prefix):
            return False

        command_part = message_text[len(self.prefix):].split()[0]
        return command_part == self.command


class CallbackDataFilter(BaseFilter):
    """Фильтр для callback данных"""

    def __init__(self, data: Optional[str] = None, contains: Optional[str] = None):
        self.data = data
        self.contains = contains

    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.callback:
            return False

        callback_data = update.message.callback.get("data", "")

        if self.data is not None and callback_data != self.data:
            return False

        if self.contains is not None and self.contains not in callback_data:
            return False

        return True


class StateFilter(BaseFilter):
    """Фильтр по состоянию FSM"""

    def __init__(self, state: Optional[str]):
        self.state = state

    async def check(self, update: Update) -> bool:
        # Проверка состояния будет реализована через middleware
        # Здесь заглушка для совместимости
        return True


class ContentTypeFilter(BaseFilter):
    """Фильтр по типу контента в сообщении"""

    def __init__(self, content_type: str):
        """
        Args:
            content_type: Тип контента (text, image, video, audio, etc.)
        """
        self.content_type = content_type

    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.body:
            return False

        body = update.message.body

        # Проверяем наличие нужного типа контента
        if self.content_type == "text":
            return bool(body.text)
        elif self.content_type == "image":
            return bool(body.attachments) and any(
                att.get("type") == "image" for att in body.attachments
            )
        elif self.content_type == "video":
            return bool(body.attachments) and any(
                att.get("type") == "video" for att in body.attachments
            )
        elif self.content_type == "audio":
            return bool(body.attachments) and any(
                att.get("type") == "audio" for att in body.attachments
            )
        elif self.content_type == "file":
            return bool(body.attachments) and any(
                att.get("type") == "file" for att in body.attachments
            )
        elif self.content_type == "contact":
            return bool(body.attachments) and any(
                att.get("type") == "contact" for att in body.attachments
            )
        elif self.content_type == "location":
            return bool(body.attachments) and any(
                att.get("type") == "location" for att in body.attachments
            )

        return False


class TextFilterFactory:
    """Фабрика для создания текстовых фильтров с удобным синтаксисом"""

    @staticmethod
    def exact(text: str) -> TextFilter:
        """Фильтр по точному совпадению текста"""
        return TextFilter(text=text)

    @staticmethod
    def contains(contains: str) -> TextFilter:
        """Фильтр по содержанию подстроки"""
        return TextFilter(contains=contains)

    @staticmethod
    def startswith(startswith: str) -> TextFilter:
        """Фильтр по началу строки"""
        return TextFilter(startswith=startswith)

    @staticmethod
    def endswith(endswith: str) -> TextFilter:
        """Фильтр по концу строки"""
        return TextFilter(endswith=endswith)

    @staticmethod
    def regex(pattern: str) -> TextFilter:
        """Фильтр по регулярному выражению"""
        return TextFilter(regex=pattern)


class CallbackFilterFactory:
    """Фабрика для создания callback фильтров"""

    @staticmethod
    def data(data: str) -> CallbackDataFilter:
        """Фильтр по точному совпадению callback данных"""
        return CallbackDataFilter(data=data)

    @staticmethod
    def contains(contains: str) -> CallbackDataFilter:
        """Фильтр по содержанию подстроки в callback данных"""
        return CallbackDataFilter(contains=contains)


class FilterFactory:
    """Фабрика для создания часто используемых фильтров"""

    def __init__(self):
        self.text = TextFilterFactory()
        self.callback = CallbackFilterFactory()

    @staticmethod
    def text_filter(exact: Optional[str] = None, contains: Optional[str] = None) -> TextFilter:
        """Создать текстовый фильтр (альтернативный метод)"""
        return TextFilter(text=exact, contains=contains)

    @staticmethod
    def command(cmd: str, prefix: str = "/") -> CommandFilter:
        """Создать фильтр команд"""
        return CommandFilter(cmd, prefix)

    @staticmethod
    def chat(*chat_ids: int) -> ChatIDFilter:
        """Создать фильтр по чатам"""
        return ChatIDFilter(list(chat_ids))

    @staticmethod
    def user(*user_ids: int) -> UserIDFilter:
        """Создать фильтр по пользователям"""
        return UserIDFilter(list(user_ids))

    @staticmethod
    def callback_filter(data: Optional[str] = None, contains: Optional[str] = None) -> CallbackDataFilter:
        """Создать фильтр callback (альтернативный метод)"""
        return CallbackDataFilter(data=data, contains=contains)

    @staticmethod
    def content(type: str) -> ContentTypeFilter:
        """Создать фильтр по типу контента"""
        return ContentTypeFilter(type)


# Удобные алиасы
F = FilterFactory()

__all__ = [
    "BaseFilter",
    "AndFilter",
    "OrFilter",
    "NotFilter",
    "TextFilter",
    "ChatIDFilter",
    "UserIDFilter",
    "CommandFilter",
    "CallbackDataFilter",
    "StateFilter",
    "ContentTypeFilter",
    "FilterFactory",
    "F",
]