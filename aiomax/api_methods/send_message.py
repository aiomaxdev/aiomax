from typing import Any, Dict, Optional, List
from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.attachments.attachments import Attachment
from aiomax.models.response_status import MessageSendResponse


class SendMessage(BaseMethod):
    method = RequestMethod.POST
    response_model = MessageSendResponse

    def __init__(
        self,
        *,
        chat_id: int | None = None,
        user_id: int | None = None,
        disable_link_preview: bool | None = True,
        text: str | None = None,
        attachments: Optional[List[Attachment]] = None,
        link: dict[str, Any] | None = None,
        notify: bool | None = True,
        format: str | None = None,
    ):
        if chat_id and user_id:
            raise ValueError("Нельзя передавать одновременно chat_id и user_id")

        if not chat_id and not user_id:
            raise ValueError("Нужно передать либо chat_id, либо user_id")

        params: Dict[str, Any] = {}

        if chat_id is not None:
            params["chat_id"] = chat_id
        else:
            params["user_id"] = user_id

        json_body: Dict[str, Any] = {}

        if text is not None:
            json_body["text"] = text

        if attachments is not None:
            json_body["attachments"] = attachments

        if link is not None:
            json_body["link"] = link

        if notify is not None:
            json_body["notify"] = notify

        if disable_link_preview is not None:
            json_body["disable_link_preview"] = disable_link_preview

        if format is not None:
            json_body["format"] = format

        path = f"{ApiEnums.MESSAGES.value}"

        super().__init__(path=path, params=params, json=json_body)