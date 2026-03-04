from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import StickerAttachmentPayload


class StickerAttachment(BaseModel):
    type: Literal[AttachmentType.STICKER]
    payload: StickerAttachmentPayload
    width: int
    height: int