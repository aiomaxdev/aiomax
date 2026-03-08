from typing import Literal

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import ContactAttachmentPayload


class ContactAttachment(BaseModel):
    type: Literal[AttachmentType.CONTACT]
    payload: ContactAttachmentPayload
