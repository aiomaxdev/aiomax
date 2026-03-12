from aiomax.api_methods.base_method import BaseMethod
from typing import List, Optional

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import GetMessagesResponse

class GetMessages(BaseMethod):
    method = RequestMethod.GET
    response_model = GetMessagesResponse

    def __init__(self, 
                 *, 
                 chat_id: int | None = None, 
                 message_ids: Optional[List[str]] = None,
                 from_timestamp: int | None = None,
                 to_timestamp: int | None = None,
                 count: int | None = None

                 ):
        if chat_id and message_ids:
            raise ValueError("Нельзя передавать одновременно chat_id и message_ids")

        if not chat_id and not message_ids:
            raise ValueError("Нужно передать либо chat_id, либо message_ids")
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        else:
            params["message_ids"] = ",".join(message_ids)
        if from_timestamp is not None:
            params["from"] = from_timestamp
        if to_timestamp is not None:
            params["to"] = to_timestamp
        if count is not None:
            params["count"] = count
        path = f"{ApiEnums.MESSAGES.value}"

        super().__init__(path=path, params = params)