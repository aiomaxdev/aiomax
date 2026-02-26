from typing import List, Optional
from aiomax.client.client import MAXClient
from aiomax.types.bot_info import BotInfo
from aiomax.types.update import Update
from aiomax.api_methods.get_me import GetMe
from aiomax.api_methods.send_message import SendMessage
from aiomax.api_methods.get_updates import GetUpdates


class Bot:
    def __init__(self, token: str):
        self.client = MAXClient(token)
        # Существующие API методы
        self._get_me = GetMe(self.client)
        self._send_message = SendMessage(self.client)
        # Новый метод
        self._get_updates = GetUpdates(self.client)

    # Существующие методы
    async def get_me(self) -> BotInfo:
        """Возвращает информацию о боте"""
        return await self._get_me.call()

    async def send_message(
        self,
        chat_id: int | None = None,
        user_id: int | None = None,
        text: str = ""
    ) -> dict:
        """Отправляет сообщение пользователю или в чат"""
        return await self._send_message.call(chat_id=chat_id, user_id=user_id, text=text)

    # Новый метод
    async def get_updates(
        self,
        offset: int | None = None,
        limit: int = 100,
        timeout: int = 30
    ) -> List[Update]:
        """Получает события из чата"""
        return await self._get_updates.call(offset=offset, limit=limit, timeout=timeout)