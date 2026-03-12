from typing import Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import GetChatMemberResponse

class GetAdminsFromChats(BaseMethod):
    method = RequestMethod.GET
    response_model = GetChatMemberResponse

    def __init__(self, *, chat_id: int):

        path = f"{ApiEnums.CHATS.value}/{chat_id}/members/admins"
        super().__init__(path=path)