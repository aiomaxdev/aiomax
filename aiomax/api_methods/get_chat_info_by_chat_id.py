from aiomax.api_methods.base_method import BaseMethod
from typing import List

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.chat import Chat

class GetChatInfoById(BaseMethod):
    method = RequestMethod.GET
    response_model = Chat


    def __init__(self, *, chat_id: int | None = None):
        params = {}
        if chat_id is not None:
            params["chatId"] = chat_id
        path = f"{ApiEnums.CHATS.value}/{chat_id}"
        super().__init__(path=path, params = params)