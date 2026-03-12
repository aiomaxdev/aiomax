from typing import List

from aiomax.api_methods.delete_bot_from_chat import DeleteBotFromChat
from aiomax.api_methods.delete_chat_by_chat_id import DeleteChatById
from aiomax.api_methods.delete_member_from_chat import DeleteMemberFromChat
from aiomax.api_methods.delete_permissions_from_chat import DeletePermissionsFromChat
from aiomax.api_methods.delete_pin_message import DeletePinMessage
from aiomax.api_methods.get_chat_admins import GetAdminsFromChats
from aiomax.api_methods.get_chat_info_by_chat_id import GetChatInfoById
from aiomax.api_methods.get_chat_members import GetMembersFromChats
from aiomax.api_methods.get_chats import GetChats
from aiomax.api_methods.get_me_from_chats import GetMeFromChats
from aiomax.api_methods.get_pinned_message import GetPinnedMessage
from aiomax.api_methods.get_updates import GetUpdates
from aiomax.api_methods.patch_chat_info_by_chat_id import PatchChatInfoById
from aiomax.api_methods.post_add_members_to_chat import PostChatMembers
from aiomax.api_methods.post_chat_actions import SendAction
from aiomax.api_methods.post_chat_admins import PostChatAdmins
from aiomax.api_methods.put_pin_message_to_chat import PutPimMessage
from aiomax.api_methods.send_message import SendMessage
from aiomax.client.client import MAXClient
from aiomax.api_methods.get_messages import GetMessages
from aiomax.api_methods.get_me import GetMe
from aiomax.models.message import Message
from aiomax.models.response_status import GetChatMemberResponse, ResponseStatus
from aiomax.models.user import BotInfo, ChatMember
from aiomax.models.chat import Chat, Chats



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
    
    async def delete_chat_by_chat_id(self, **kwargs)->ResponseStatus:
        return await self(DeleteChatById(**kwargs))  
    
    async def send_message(self, **kwargs):
        return await self(SendMessage(**kwargs))
    
    async def send_action(self, **kwargs)->ResponseStatus:
        return await self(SendAction(**kwargs))
    
    async def get_pinned_message(self, **kwargs) ->Message:
        return await self(GetPinnedMessage(**kwargs))
    
    async def pin_message(self, **kwargs) ->ResponseStatus:
        return await self(PutPimMessage(**kwargs))
    
    async def unpin_message(self, **kwargs) ->ResponseStatus:
        return await self(DeletePinMessage(**kwargs))
    
    async def get_me_from_chat(self, **kwargs) -> ChatMember:
        return await self(GetMeFromChats(**kwargs))
    
    async def delete_bot_from_chat(self, **kwargs) -> ResponseStatus:
        return await self(DeleteBotFromChat(**kwargs))
    
    async def get_admins_from_chat(self, **kwargs) -> GetChatMemberResponse:
        return await self(GetAdminsFromChats(**kwargs))
    
    async def add_admins_to_chat(self, **kwargs) -> ResponseStatus:
        return await self(PostChatAdmins(**kwargs))
    
    async def delete_permissions_from_chat(self, **kwargs) -> ResponseStatus:
        return await self(DeletePermissionsFromChat(**kwargs))
    
    async def get_members_from_chat(self, **kwargs) -> GetChatMemberResponse:
        return await self(GetMembersFromChats(**kwargs))
    
    async def add_members_to_chat(self, **kwargs):
        return await self(PostChatMembers(**kwargs))
    
    async def delete_members_from_chat(self, **kwargs) -> ResponseStatus:
        return await self(DeleteMemberFromChat(**kwargs))

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