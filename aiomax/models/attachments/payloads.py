from typing import List, Optional, Union

from pydantic import BaseModel

from aiomax.models.keyboard.callback_button import CallbackButton
from aiomax.models.keyboard.link_button import LinkButton
from aiomax.models.keyboard.message_button import MessageButton
from aiomax.models.keyboard.open_app_button import OpenAppButton
from aiomax.models.keyboard.request_contact_button import RequestContactButton
from aiomax.models.keyboard.request_geo_locatiom_button import RequestGeoLocationButton
from aiomax.models.user import User


class PhotoAttachmentPayload(BaseModel):
    photo_id: int
    token: str
    url: str


class MediaAttachmentPayload(BaseModel):
    url: str
    token: str


class FileAttachmentPayload(BaseModel):
    url: str
    token: str


class StickerAttachmentPayload(BaseModel):
    url: str
    code: str


class ContactAttachmentPayload(BaseModel):
    vcf_info: Optional[str] = None
    max_info: Optional[User] = None


class InlineKeyboardPayload(BaseModel):
    buttons: List[List[Union[
    CallbackButton,
    LinkButton,
    RequestGeoLocationButton,
    RequestContactButton,
    OpenAppButton,
    MessageButton
]]] 

class ShareAttachmentPayload(BaseModel):
    url: Optional[str] = None
    code: Optional[str] = None
