from typing import Dict, List, Optional

from pydantic import BaseModel

from aiomax.enums.chat_status_enum import ChatStatus
from aiomax.enums.chat_type import ChatType
from aiomax.models.user import UserWithPhoto
from aiomax.models.message import Message


class ChatIcon(BaseModel):
    url:str

class Chat(BaseModel):
    chat_id: int
    type: ChatType
    status: ChatStatus
    title: Optional[str] = None
    icon: ChatIcon
    last_event_time: int
    participants_count: int
    owner_id: Optional[int] = None
    participants: Optional[Dict[str]]
    is_public: bool
    link: Optional[str] = None
    description: Optional[str] = None
    dialog_with_user: Optional[UserWithPhoto] = None
    chat_message_id: Optional[str] = None
    pinned_message: Optional[Message] = None
    
class GetChatsResponse(BaseModel):
    chats: List[Chat]
    marker: Optional[int]
