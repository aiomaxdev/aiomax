from typing import Literal

from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class MessageButton(BaseModel):
    type: Literal[ButtonType.MESSAGE]
    text: str
