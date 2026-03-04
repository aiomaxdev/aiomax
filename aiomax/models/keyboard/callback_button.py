from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class CallbackButton(BaseModel):
    type: ButtonType.CALLBACK
    text: str
    payload: str
