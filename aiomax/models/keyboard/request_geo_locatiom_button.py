from typing import Optional

from pydantic import BaseModel

from aiomax.enums.button_type_enum import ButtonType


class RequestGeoLocationButton(BaseModel):
    type: ButtonType.REQUEST_GEO_LOCATION
    text: str
    quick: Optional[bool]= False
