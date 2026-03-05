from aiomax.api_methods.base_method import BaseMethod
from typing import List

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.chat import GetChatsResponse

class GetChatById(BaseMethod):
    path = ApiEnums.CHATS
    method = RequestMethod.GET


    def __init__(self, *, chat_id: int | None = None):
        params = {}
        if chat_id is not None:
            params["chatId"] = chat_id
        super().__init__(params = params)