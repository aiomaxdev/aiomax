from typing import Any, Dict, Optional, List
from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.attachments.attachments import Attachment
from aiomax.models.response_status import ResponseStatus


class EditMessage(BaseMethod):
    method = RequestMethod.PUT
    response_model = ResponseStatus

    def __init__(
        self,
        *,
        message_id: int | None = None,
        text: str | None = None,
        attachments: Attachment | None = None, 
        link: dict[str, Any] | None = None,
        notify: bool | None = True,
        format: str | None = None,
    ):

        params: Dict[str, Any] = {}

        if message_id is not None:
            params["message_id"] = message_id

        json_body: Dict[str, Any] = {}

        if text is not None:
            json_body["text"] = text

        if attachments is not None:
            json_body["attachments"] = attachments

        if link is not None:
            json_body["link"] = link

        if notify is not None:
            json_body["notify"] = notify

        if format is not None:
            json_body["format"] = format

        path = f"{ApiEnums.MESSAGES.value}"

        super().__init__(path=path, params=params, json=json_body)