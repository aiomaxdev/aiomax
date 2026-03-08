from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import MediaAttachmentPayload


class LocationAttachment(BaseModel):
    type: Literal[AttachmentType.LOCATION]
    latitude: float
    longitude: float