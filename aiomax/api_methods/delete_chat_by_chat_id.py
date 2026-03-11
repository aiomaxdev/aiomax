from aiomax.api_methods.base_method import BaseMethod
from typing import Any, Dict, List, Optional

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.attachments.image import PhotoAttachmentRequestPayload
from aiomax.models.response_status import ResponseStatus

class DeleteChatById(BaseMethod):
    method = RequestMethod.DELETE
    response_model = ResponseStatus


    def __init__(self, 
                 *, 
                 chat_id: int | None = None,
                 ):

        path = f"{ApiEnums.CHATS.value}/{chat_id}"

        super().__init__(path=path)