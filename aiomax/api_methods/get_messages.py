from aiomax.api_methods.base_method import BaseMethod
from typing import List

class GetMessages(BaseMethod):
    path = "messages"
    method = "GET"

    def __init__(self, *, chat_id: str = None, message_ids: List[str] = None):
        if chat_id and message_ids:
            raise ValueError("Нельзя передавать одновременно chat_id и message_ids")

        if not chat_id and not message_ids:
            raise ValueError("Нужно передать либо chat_id, либо message_ids")
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        else:
            params["message_ids"] = ",".join(message_ids)
        super().__init__(params = params)