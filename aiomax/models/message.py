from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from aiomax.enums.chat_type import ChatType
from aiomax.enums.message_link_type_enum import MessageLinkType
from aiomax.enums.text_style_enum import TextStyle
from aiomax.models.attachments.audio import AudioAttachment
from aiomax.models.attachments.contact import ContactAttachment
from aiomax.models.attachments.file import FileAttachment
from aiomax.models.attachments.image import ImageAttachment, PhotoAttachmentRequestPayload
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

class MarkupElementBase(BaseModel):
    from_: int = Field(..., alias="from")
    length: int

    model_config = {"populate_by_name": True}

class StrongMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.STRONG]


class EmphasizedMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.EMPHASIZED]


class MonospacedMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.MONOSPACED]

class StrikethroughMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.STRIKETHROUGH]


class UnderlineMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.UNDERLINE]

class LinkMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.LINK]
    url: str

class UserMentionMarkupElement(MarkupElementBase):
    type: Literal[TextStyle.USER_MENTION]
    user_link: Optional[str] = None
    user_id: Optional[int] = None

class MessageStat (BaseModel):
    views:int

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
            StrongMarkupElement,
            EmphasizedMarkupElement,
            MonospacedMarkupElement,
            StrikethroughMarkupElement,
            UnderlineMarkupElement,
            LinkMarkupElement,
            UserMentionMarkupElement
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
    link: Optional[LinkedMessage]= None
    body: MessageBody
    stat: Optional[MessageStat]= None
    url: Optional[str]= None

class NewMessageLink(BaseModel):
    type: MessageLinkType
    mid: str

class AttachmentRequest(BaseModel):
    type: str  
    payload: PhotoAttachmentRequestPayload

class NewMessageBody(BaseModel):
    text: Optional[str] = Field(default=None, max_length=4000)
    attachments: Optional[List[AttachmentRequest]] = None
    link: Optional[NewMessageLink] = None

    notify: Optional[bool] = True

    format: Optional[Literal["markdown", "html"]] = None