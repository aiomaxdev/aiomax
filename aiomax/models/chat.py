from typing import Dict, Optional

from pydantic import BaseModel

from aiomax.enums.chat_status_enum import ChatStatus
from aiomax.enums.chat_type import ChatType
from aiomax.models.user import UserWithPhoto


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