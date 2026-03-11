from typing import Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import GetChatAdminsResponse

class GetMembersFromChats(BaseMethod):
    method = RequestMethod.GET
    response_model = GetChatAdminsResponse

    def __init__(self, *, chat_id: int):

        path = f"{ApiEnums.CHATS.value}/{chat_id}/members/admins"
        super().__init__(path=path)