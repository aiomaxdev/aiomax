from typing import Optional

from pydantic import BaseModel

from aiomax.models.message import Message


class ResponseStatus(BaseModel):
    success:bool
    message: Optional[str] = None

class GetPinnedMessageResponse(BaseModel):
    message: Message | None = None