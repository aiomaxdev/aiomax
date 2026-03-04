from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class LinkButton(BaseModel):
    type: ButtonType.LINK
    text: str
    url: str
