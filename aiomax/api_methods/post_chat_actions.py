from typing import Any, Dict, Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.chat_action_enums import ChatAction
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import ResponseStatus


class SendAction(BaseMethod):
    method: str = RequestMethod.POST
    response_model = ResponseStatus

    def __init__(self, *, 
                 chat_id: int | None = None, 
                 action: ChatAction = ChatAction.TYPING, 

                 ):
        if not chat_id:
            raise ValueError("Нужно передать chat_id")
        params: Dict[str, Any]={}
        params["chat_id"] = chat_id

        json_body: Dict[str, Any]={}
        json_body["action"] = action

        path = f"{ApiEnums.CHATS.value}/{chat_id}/actions"
        super().__init__(path=path,params = params, json = json_body)