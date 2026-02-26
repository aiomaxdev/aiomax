from typing import Optional, List
from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: bool
    last_activity_time: Optional[int] = None
    name: Optional[str] = None  # устаревшее


class Recipient(BaseModel):
    chat_id: Optional[int] = None
    chat_type: Optional[str] = None  # "chat" или "dialog"
    user_id: Optional[int] = None


class PhotoAttachmentPayload(BaseModel):
    photo_id: int
    token: str
    url: str


class Attachment(BaseModel):
    type: str
    payload: Optional[PhotoAttachmentPayload] = None


class MarkupElement(BaseModel):
    type: str
    from_: int = Field(..., alias="from")  # "from" — ключ в JSON, но "from_" в Python
    length: int


class MessageStat(BaseModel):
    views: Optional[int] = None
    url: Optional[str] = None


class MessageBody(BaseModel):
    mid: str
    seq: int
    text: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    markup: Optional[List[MarkupElement]] = None


class Message(BaseModel):
    chat_id: Optional[int] = None
    sender: Optional[User] = None
    recipient: Optional[Recipient] = None
    timestamp: Optional[int] = None
    link: Optional[dict] = None  # можно потом вынести в отдельный класс LinkedMessage
    body: Optional[MessageBody] = None
    stat: Optional[MessageStat] = None
    url: Optional[str] = None