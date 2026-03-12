from typing import List, Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import GetChatMemberResponse

class GetMembersFromChats(BaseMethod):
    method = RequestMethod.GET
    response_model = GetChatMemberResponse

    def __init__(self, *,
                chat_id: int, 
                user_ids: Optional[List[int]] = None,           
                marker: Optional[int] = None,
                count: Optional[int] = 20):
        if count < 1 or count > 100:
            raise ValueError("count must be between 1 and 100")

        params = {}
        if user_ids:
            params["user_ids"] = user_ids
        else:
            if marker is not None:
                params["marker"] = marker
            params["count"] = count
        path = f"{ApiEnums.CHATS.value}/{chat_id}/members"
        super().__init__(path=path, params=params)