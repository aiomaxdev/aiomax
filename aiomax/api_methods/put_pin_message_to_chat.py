from aiomax.api_methods.base_method import BaseMethod
from typing import Any, Dict, Optional
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import ResponseStatus

class PutPimMessage(BaseMethod):
    method = RequestMethod.PUT
    response_model = ResponseStatus


    def __init__(self, 
                 *, 
                 chat_id: int | None = None,
                 message_id:str,
                 notify: bool | None = None
                 ):
        params = {}
        path = f"{ApiEnums.CHATS.value}/{chat_id}/pin"

        json_body: Dict[str, Any]={}
        if message_id is not None:
            json_body["message_id"] = message_id
        elif notify is not None:
            json_body["notify"] = notify
        super().__init__(path=path, params=params, json = json_body)