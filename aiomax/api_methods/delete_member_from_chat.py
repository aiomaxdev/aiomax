from typing import Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import ResponseStatus

class DeleteMemberFromChat(BaseMethod):
    method = RequestMethod.DELETE
    response_model = ResponseStatus


    def __init__(self, 
                 *, 
                chat_id: int,
                user_id: int,
                block: Optional[bool]=None
    ):
        if chat_id is None:
            raise ValueError("Нужно передать chat_id")

        if user_id is None:
            raise ValueError("Нужно передать user_id")
        params = {}
        if user_id is not None:
            params["user_id"] = user_id
        if block is not None:
            params["block"] = block
        path = f"{ApiEnums.CHATS.value}/{chat_id}/members"

        super().__init__(path=path, params=params)