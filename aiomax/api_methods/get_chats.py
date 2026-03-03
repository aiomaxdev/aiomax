from typing import Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.user import BotInfo

class GetChats(BaseMethod):
    path = ApiEnums.CHATS
    method = RequestMethod.GET
    # response_model = BotInfo

    def __init__(self, *, count: Optional[int] = 50, marker:Optional[int] = None ):
        
        params = {}
        if count is not None:
            params["count"] = count
        else:
            params["marker"] = marker
        super().__init__()