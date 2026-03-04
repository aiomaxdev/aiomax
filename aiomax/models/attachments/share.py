from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import ShareAttachmentPayload


class ShareAttachment(BaseModel):
    type: Literal[AttachmentType.AUDIO]
    payload: ShareAttachmentPayload
    title: Optional[str]= None
    description: Optional[str]= None
    image_url: Optional[str]= None