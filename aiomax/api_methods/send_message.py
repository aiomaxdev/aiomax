from typing import Any, Dict, Optional

from aiomax.api_methods.base_method import BaseMethod


class SendMessage(BaseMethod):
    path = "messages"
    method = "POST"

    def __init__(self, *, 
                 chat_id: str = None, 
                 user_id: str = None, 
                 text: Optional[str] = None,
                 attachments: Optional[list] = None,
                 link: Dict[str, Any]={},
                 notify: bool = True,
                 format: str =None
                 ):
        if chat_id and user_id:
            raise ValueError("Нельзя передавать одновременно chat_id и message_ids")
        if not chat_id and not user_id:
            raise ValueError("Нужно передать либо chat_id, либо message_ids")
        params: Dict[str, Any]={}
        if chat_id:
            params["chat_id"] = chat_id
        else:
            params["user_id"] = user_id
        json_body: Dict[str, Any]={}
        json_body["text"] =text
        json_body["attachments"] = attachments
        json_body["link"] = link
        json_body["notify"] = notify
        json_body["format"] = format
        super().__init__(params = params, json = json_body)