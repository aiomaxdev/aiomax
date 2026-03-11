from typing import List, Optional

from pydantic import BaseModel

from aiomax.models.message import Message
from aiomax.models.user import ChatMember


class ResponseStatus(BaseModel):
    success:bool
    message: Optional[str] = None

class GetPinnedMessageResponse(BaseModel):
    message: Message | None = None

class GetChatAdminsResponse(BaseModel):
    members: List[ChatMember]
    marker: Optional[int] = None