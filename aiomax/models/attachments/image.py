from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import PhotoAttachmentPayload


class ImageAttachment(BaseModel):
    type: Literal[AttachmentType.IMAGE]
    payload: PhotoAttachmentPayload

class PhotoAttachmentRequestPayload(BaseModel):
    url: Optional[str]=None
    token: Optional[str]=None
    photos: Optional[str]=None