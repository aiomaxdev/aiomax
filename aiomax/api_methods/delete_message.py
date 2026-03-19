from typing import Any, Dict, Optional, List
from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.attachments.attachments import Attachment
from aiomax.models.response_status import ResponseStatus


class DeleteMessage(BaseMethod):
    method = RequestMethod.DELETE
    response_model = ResponseStatus

    def __init__(
        self,
        *,
        message_id: int | None = None,
    ):
        params: Dict[str, Any] = {}
        if message_id is not None:
            params["message_id"] = message_id
        path = f"{ApiEnums.MESSAGES.value}"
        super().__init__(path=path, params=params)