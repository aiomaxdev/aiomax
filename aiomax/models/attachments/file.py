from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import FileAttachmentPayload


class FileAttachment(BaseModel):
    type: Literal[AttachmentType.FILE]
    payload: FileAttachmentPayload
    filename: str
    size: int