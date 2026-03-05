from typing import Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.chat import Chat, GetChatsResponse


class GetChats(BaseMethod):
    path = ApiEnums.CHATS
    method = RequestMethod.GET
    response_model = GetChatsResponse

    def __init__(self, *, count: Optional[int] = 50, marker:Optional[int] = None ):
        
        params = {}
        if count is not None:
            params["count"] = count
        if marker is not None:
            params["marker"] = marker
        super().__init__(params = params)