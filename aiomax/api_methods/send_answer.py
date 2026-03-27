from typing import Any, Dict, Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.message import NewMessageBody
from aiomax.models.response_status import ResponseStatus



class SendAnswer(BaseMethod):
    method = RequestMethod.POST
    response_model = ResponseStatus

    def __init__(
        self,
        *,
        callback_id: str,
        message: Optional[NewMessageBody] = None,
        notification: Optional[str] = None,
    ):
        if not callback_id:
            raise ValueError("callback_id обязателен")

        params: Dict[str, Any] = {
            "callback_id": callback_id
        }

        json_body: Dict[str, Any] = {}

        if message is not None:
            if isinstance(message, dict):
                json_body["message"] = message
            else:
                json_body["message"] = message.model_dump(exclude_none=True)
        if notification is not None:
            json_body["notification"] = notification

        path = ApiEnums.ANSWERS.value 

        super().__init__(path=path, params=params, json=json_body)