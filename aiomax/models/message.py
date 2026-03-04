from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from aiomax.enums.chat_type import ChatType
from aiomax.enums.message_link_type_enum import MessageLinkType
from aiomax.enums.text_style_enum import TextStyle
from aiomax.models.attachments.audio import AudioAttachment
from aiomax.models.attachments.contact import ContactAttachment
from aiomax.models.attachments.file import FileAttachment
from aiomax.models.attachments.image import ImageAttachment
from aiomax.models.attachments.inline_keyboard import InlineKeyboardAttachment
from aiomax.models.attachments.location import LocationAttachment
from aiomax.models.attachments.share import ShareAttachment
from aiomax.models.attachments.sticker import StickerAttachment
from aiomax.models.attachments.video import VideoAttachment
from aiomax.models.user import User

class Recipient(BaseModel):
    chat_id: Optional[int]= None
    chat_type: ChatType
    user_id: Optional[int]= None

class BaseMarkupElement(BaseModel):
    type: TextStyle
    from_: int = Field(..., alias="from")
    length: int

    model_config = {"populate_by_name": True}


class LinkMarkupElement(BaseMarkupElement):
    type: Literal[TextStyle.LINK]
    url: str


class MessageStat (BaseModel):
    views:int

class UserMentionMarkupElement(BaseMarkupElement):
    type: Literal[TextStyle.USER_MENTION]
    user_link: Optional[str] = None
    user_id: Optional[int] = None

class MessageBody(BaseModel):
    mid: str
    seq: int
    text: Optional[str] = None

    attachments: Optional[List[Annotated[
        Union[
            ImageAttachment,
            VideoAttachment,
            AudioAttachment,
            FileAttachment,
            StickerAttachment,
            ContactAttachment,
            InlineKeyboardAttachment,
            ShareAttachment,
            LocationAttachment
        ],
        Field(discriminator="type")
    ]]] = None

    markup: Optional[List[Annotated[
        Union[
            BaseMarkupElement,        # обычные стили: STRONG, EMPHASIZED, MONOSPACED, STRIKETHROUGH, UNDERLINE
            LinkMarkupElement,        # link
            UserMentionMarkupElement  # user_mention
        ],
        Field(discriminator="type")
    ]]] = None
        
    
class LinkedMessage(BaseModel):
    type: MessageLinkType
    sender: Optional[User]= None
    chat_id: Optional[int]= None
    message: MessageBody

class Message(BaseModel):
    sender: Optional[User]= None
    recipient: Recipient
    timestamp: int
    link: LinkedMessage
    body: MessageBody
    stat: Optional[MessageStat]= None
    url: Optional[str]= None

