from typing import Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.chat import Chats
from aiomax.models.user import ChatMember


class GetMeFromChats(BaseMethod):
    method = RequestMethod.GET
    response_model = ChatMember

    def __init__(self, *, chat_id: int):

        path = f"{ApiEnums.CHATS.value}/{chat_id}/members/me"
        super().__init__(path=path)