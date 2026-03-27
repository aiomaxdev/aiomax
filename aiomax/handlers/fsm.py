from typing import Any, Dict, Optional
from aiomax.handlers.handler import BaseFilter, State


class FSMContext:
    """
    Контекст конечного автомата (FSM) для хранения состояния пользователя.
    Аналог FSM в aiogram.
    
    Пример использования:
        class MyStates(StatesGroup):
            waiting_for_name = State()
            waiting_for_age = State()
        
        @router.on_message(F.Command("/start"))
        async def start(event, context, fsm: FSMContext):
            await fsm.set_state(MyStates.waiting_for_name)
            await bot.send_message(chat_id=event["chat_id"], text="Введите ваше имя:")
        
        @router.on_message(F.State(MyStates.waiting_for_name))
        async def get_name(event, context, fsm: FSMContext):
            name = event["message"]["body"]["text"]
            await fsm.set_data({"name": name})
            await fsm.set_state(MyStates.waiting_for_age)
            await bot.send_message(chat_id=event["chat_id"], text="Введите ваш возраст:")
    """
    
    def __init__(self, storage: "BaseStorage", user_id: int, chat_id: Optional[int] = None):
        self.storage = storage
        self.user_id = user_id
        self.chat_id = chat_id or user_id
        self._key = f"{user_id}:{chat_id}"
    
    async def get_state(self) -> Optional[str]:
        """Получить текущее состояние"""
        data = await self.storage.get(self._key)
        return data.get("state") if data else None
    
    async def set_state(self, state: str) -> None:
        """Установить новое состояние"""
        data = await self.storage.get(self._key) or {}
        data["state"] = state
        await self.storage.set(self._key, data)
    
    async def reset_state(self) -> None:
        """Сбросить состояние"""
        data = await self.storage.get(self._key) or {}
        data["state"] = None
        await self.storage.set(self._key, data)
    
    async def get_data(self) -> Dict[str, Any]:
        """Получить данные контекста"""
        data = await self.storage.get(self._key)
        return data.get("data", {}) if data else {}
    
    async def set_data(self, data: Dict[str, Any]) -> None:
        """Установить данные контекста"""
        current = await self.storage.get(self._key) or {}
        current["data"] = data
        await self.storage.set(self._key, current)
    
    async def update_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновить данные контекста"""
        current = await self.storage.get(self._key) or {}
        current_data = current.get("data", {})
        current_data.update(data)
        current["data"] = current_data
        await self.storage.set(self._key, current)
        return current_data


class BaseStorage:
    """Базовый класс для хранилища состояний FSM"""
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Получить данные по ключу"""
        raise NotImplementedError
    
    async def set(self, key: str, data: Dict[str, Any]) -> None:
        """Установить данные по ключу"""
        raise NotImplementedError
    
    async def delete(self, key: str) -> None:
        """Удалить данные по ключу"""
        raise NotImplementedError


class MemoryStorage(BaseStorage):
    """
    Хранилище состояний в памяти.
    Подходит для тестирования и простых ботов.
    Для продакшена используйте RedisStorage.
    """
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._storage.get(key)
    
    async def set(self, key: str, data: Dict[str, Any]) -> None:
        self._storage[key] = data
    
    async def delete(self, key: str) -> None:
        if key in self._storage:
            del self._storage[key]
    
    async def clear(self) -> None:
        """Очистить всё хранилище"""
        self._storage.clear()
