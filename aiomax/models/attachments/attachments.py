from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from aiomax.models.attachments.audio import AudioAttachment
from aiomax.models.attachments.contact import ContactAttachment
from aiomax.models.attachments.file import FileAttachment
from aiomax.models.attachments.image import ImageAttachment
from aiomax.models.attachments.inline_keyboard import InlineKeyboardAttachment
from aiomax.models.attachments.location import LocationAttachment
from aiomax.models.attachments.share import ShareAttachment
from aiomax.models.attachments.sticker import StickerAttachment
from aiomax.models.attachments.video import VideoAttachment


class Attachment(BaseModel):
    items: Optional[List[Annotated[
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
