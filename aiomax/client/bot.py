from typing import List

from aiomax.api_methods.delete_chat_by_chat_id import DeleteChatById
from aiomax.api_methods.get_chat_info_by_chat_id import GetChatInfoById
from aiomax.api_methods.get_chats import GetChats
from aiomax.api_methods.get_updates import GetUpdates
from aiomax.api_methods.patch_chat_info_by_chat_id import PatchChatInfoById
from aiomax.api_methods.send_message import SendMessage
from aiomax.client.client import MAXClient
from aiomax.api_methods.get_messages import GetMessages
from aiomax.api_methods.get_me import GetMe
from aiomax.models.user import BotInfo
from aiomax.models.chat import Chat, ChatDelete, Chats



class Bot:
    def __init__(self, token: str):
        self.client = MAXClient(token)
        self._marker: int | None = None
        self._is_running = False

    async def start(self):
        await self.client.start()

    async def close(self):
        await self.client.close()

    async def __call__(self, method):
        return await self.client.request(method)

    # сахарок
    async def get_me(self) -> BotInfo:
        return await self(GetMe())

    async def get_messages(self, **kwargs):
        return await self(GetMessages(**kwargs))
    
    async def get_updates(self, **kwargs):
        return await self(GetUpdates(**kwargs))
        
    async def get_chats(self, **kwargs) ->Chats:
        return await self(GetChats(**kwargs))
    
    async def get_chat_info_by_chat_id(self, **kwargs) -> Chat:
        return await self(GetChatInfoById(**kwargs))    
    
    async def patch_chat_info_by_chat_id(self, **kwargs) -> Chat:
        return await self(PatchChatInfoById(**kwargs))  
    
    async def delete_chat_by_chat_id(self, **kwargs)->ChatDelete:
        return await self(DeleteChatById(**kwargs))  
    
    async def send_message(self, **kwargs):
        return await self(SendMessage(**kwargs))
    
    async def start_polling(self, *, limit:int =100, timeout: int = 30, types: List[str]| None =None):
        self._is_running = True
        while self._is_running:
            response = await self.get_updates(
                marker = self._marker,
                limit = limit,
                timeout = timeout,
                types = types
            )
            updates = response.get("updates",[])
            # print(updates)
            self._marker = response.get("marker")
            
            for update in updates:
                yield await self.update_poll(update)

    async def stop_polling(self):
        self._is_running = False

    async def update_poll(self, update:dict):
        return update