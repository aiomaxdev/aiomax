from typing import List, Optional

from pydantic import BaseModel

from aiomax.models.message import Message
from aiomax.models.user import ChatMember


class ResponseStatus(BaseModel):
    success:bool
    message: Optional[str] = None

class GetPinnedMessageResponse(BaseModel):
    message: Message | None = None

class GetChatMemberResponse(BaseModel):
    members: List[ChatMember]
    marker: Optional[int] = None

class FailedUserDetail(BaseModel):
    error_code: str
    user_ids: List[int]

class AddMembersToChat(BaseModel):
    success: bool
    message: Optional[str] = None
    failed_user_ids: Optional[List[int]] = None
    failed_user_details: Optional[List[FailedUserDetail]] = None

class GetMessagesResponse(BaseModel):
    messages: List[Message]

class MessageSendResponse(BaseModel):
    message:Message

