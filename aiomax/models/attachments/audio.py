from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import MediaAttachmentPayload


class AudioAttachment(BaseModel):
    type: Literal[AttachmentType.AUDIO]
    payload: MediaAttachmentPayload
    transcription: Optional[str]= None