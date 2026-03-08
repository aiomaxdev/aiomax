from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import MediaAttachmentPayload

class VideoThumbnail(BaseModel):
    url:str


class VideoAttachment(BaseModel):
    type: Literal[AttachmentType.VIDEO]
    payload: MediaAttachmentPayload
    thumbnail: Optional[VideoThumbnail]
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
