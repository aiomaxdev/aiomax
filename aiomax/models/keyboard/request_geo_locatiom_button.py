from typing import Literal, Optional

from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class RequestGeoLocationButton(BaseModel):
    type: Literal[ButtonType.REQUEST_GEO_LOCATION]
    text: str
    quick: Optional[bool]= False
