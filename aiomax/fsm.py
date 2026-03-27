"""
FSM (Finite State Machine) для управления состояниями диалога.

Позволяет создавать многошаговые сценарии взаимодействия с пользователем.
"""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Базовый класс для хранилища состояний"""

    @abstractmethod
    async def get_state(self, user_id: int, chat_id: Optional[int] = None) -> Optional[str]:
        """Получить состояние пользователя"""
        pass

    @abstractmethod
    async def set_state(self, user_id: int, state: Optional[str], chat_id: Optional[int] = None) -> None:
        """Установить состояние пользователя"""
        pass

    @abstractmethod
    async def get_data(self, user_id: int, chat_id: Optional[int] = None) -> Dict[str, Any]:
        """Получить данные пользователя"""
        pass

    @abstractmethod
    async def set_data(self, user_id: int, data: Dict[str, Any], chat_id: Optional[int] = None) -> None:
        """Установить данные пользователя"""
        pass

    @abstractmethod
    async def update_data(self, user_id: int, data: Dict[str, Any], chat_id: Optional[int] = None) -> None:
        """Обновить данные пользователя (частичное обновление)"""
        pass

    @abstractmethod
    async def clear(self, user_id: int, chat_id: Optional[int] = None) -> None:
        """Очистить состояние и данные пользователя"""
        pass


class MemoryStorage(BaseStorage):
    """Хранилище состояний в памяти (для тестирования и простых случаев)"""

    def __init__(self):
        self._states: Dict[str, Optional[str]] = {}
        self._data: Dict[str, Dict[str, Any]] = {}

    def _get_key(self, user_id: int, chat_id: Optional[int] = None) -> str:
        if chat_id is not None:
            return f"{chat_id}:{user_id}"
        return str(user_id)

    async def get_state(self, user_id: int, chat_id: Optional[int] = None) -> Optional[str]:
        key = self._get_key(user_id, chat_id)
        return self._states.get(key)

    async def set_state(self, user_id: int, state: Optional[str], chat_id: Optional[int] = None) -> None:
        key = self._get_key(user_id, chat_id)
        if state is None:
            self._states.pop(key, None)
        else:
            self._states[key] = state

    async def get_data(self, user_id: int, chat_id: Optional[int] = None) -> Dict[str, Any]:
        key = self._get_key(user_id, chat_id)
        return self._data.get(key, {}).copy()

    async def set_data(self, user_id: int, data: Dict[str, Any], chat_id: Optional[int] = None) -> None:
        key = self._get_key(user_id, chat_id)
        self._data[key] = data.copy()

    async def update_data(self, user_id: int, data: Dict[str, Any], chat_id: Optional[int] = None) -> None:
        key = self._get_key(user_id, chat_id)
        if key not in self._data:
            self._data[key] = {}
        self._data[key].update(data)

    async def clear(self, user_id: int, chat_id: Optional[int] = None) -> None:
        key = self._get_key(user_id, chat_id)
        self._states.pop(key, None)
        self._data.pop(key, None)


class StatesGroup:
    """
    Базовый класс для групп состояний.

    Пример использования:
        class RegistrationStates(StatesGroup):
            name = State()
            age = State()
            phone = State()
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._states = {}

    def __init__(self):
        raise TypeError("StatesGroup cannot be instantiated. Use it as a base class.")

    @classmethod
    def get_states(cls) -> Dict[str, str]:
        """Получить все состояния группы"""
        return cls._states.copy()

    @classmethod
    def get_state_name(cls, state_attr: str) -> str:
        """Получить имя состояния по атрибуту"""
        return cls._states.get(state_attr, f"{cls.__name__}:{state_attr}")


class State:
    """Класс для представления состояния"""

    def __init__(self):
        self._name: Optional[str] = None

    def __set_name__(self, owner: type, name: str):
        self._name = f"{owner.__name__}:{name}"
        if hasattr(owner, '_states'):
            owner._states[name] = self._name

    def __str__(self) -> str:
        return self._name or ""

    def __repr__(self) -> str:
        return f"State({self._name!r})"


class FSMManager:
    """Менеджер для управления состояниями FSM"""

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    async def get_state(self, user_id: int, chat_id: Optional[int] = None) -> Optional[str]:
        """Получить текущее состояние пользователя"""
        return await self.storage.get_state(user_id, chat_id)

    async def set_state(self, user_id: int, state: Optional[str], chat_id: Optional[int] = None) -> None:
        """Установить состояние пользователя"""
        await self.storage.set_state(user_id, state, chat_id)

    async def finish(self, user_id: int, chat_id: Optional[int] = None) -> None:
        """Завершить FSM (сбросить состояние)"""
        await self.storage.set_state(user_id, None, chat_id)

    async def get_data(self, user_id: int, chat_id: Optional[int] = None) -> Dict[str, Any]:
        """Получить данные пользователя"""
        return await self.storage.get_data(user_id, chat_id)

    async def set_data(self, user_id: int, data: Dict[str, Any], chat_id: Optional[int] = None) -> None:
        """Установить данные пользователя"""
        await self.storage.set_data(user_id, data, chat_id)

    async def update_data(self, user_id: int, data: Dict[str, Any], chat_id: Optional[int] = None) -> None:
        """Обновить данные пользователя"""
        await self.storage.update_data(user_id, data, chat_id)

    async def clear(self, user_id: int, chat_id: Optional[int] = None) -> None:
        """Очистить состояние и данные пользователя"""
        await self.storage.clear(user_id, chat_id)


__all__ = [
    "BaseStorage",
    "MemoryStorage",
    "StatesGroup",
    "State",
    "FSMManager",
]