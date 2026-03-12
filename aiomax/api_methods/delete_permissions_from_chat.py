from aiomax.api_methods.base_method import BaseMethod
from typing import Any, Dict, List, Optional

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import ResponseStatus

class DeletePermissionsFromChat(BaseMethod):
    method = RequestMethod.DELETE
    response_model = ResponseStatus


    def __init__(self, 
                 *, 
                chat_id: int,
                user_id: int
    ):
        if chat_id is None:
            raise ValueError("Нужно передать chat_id")

        if user_id is None:
            raise ValueError("Нужно передать user_id")
        path = f"{ApiEnums.CHATS.value}/{chat_id}/members/admins/{user_id}"

        super().__init__(path=path)