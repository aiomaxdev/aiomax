from typing import Literal

from pydantic import BaseModel

from aiomax.enums.attachment_type_enum import AttachmentType
from aiomax.models.attachments.payloads import InlineKeyboardPayload



class InlineKeyboardAttachment(BaseModel):
    type: Literal[AttachmentType.INLINE_KEYBOARD]
    payload: InlineKeyboardPayload
