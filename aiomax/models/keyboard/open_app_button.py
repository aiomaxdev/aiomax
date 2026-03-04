from typing import Optional

from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class OpenAppButton(BaseModel):
    type: ButtonType.OPEN_APP
    text: str
    web_app: Optional[str]=None
    contact_id: Optional[int]=None
    payload: Optional[str]= None

