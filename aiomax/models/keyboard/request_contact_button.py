from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class RequestContactButton(BaseModel):
    type: ButtonType.REQUEST_CONTACT
    text: str
