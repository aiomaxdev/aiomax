from aiomax.api_methods.base_method import BaseMethod
from typing import Any, Dict, List, Optional

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.attachments.image import PhotoAttachmentRequestPayload
from aiomax.models.chat import Chat

class PatchChatInfoById(BaseMethod):
    method = RequestMethod.PATCH
    response_model = Chat


    def __init__(self, 
                 *, 
                 chat_id: int | None = None,
                 icon:Optional[PhotoAttachmentRequestPayload]=None,
                 title:Optional[str]=None,
                 pin:Optional[str]=None,
                 notify: Optional[bool]=None
                 ):
        params = {}
        path = f"{ApiEnums.CHATS.value}/{chat_id}"

        json_body: Dict[str, Any]={}
        if pin is not None:
            json_body["pin"] = pin
        elif icon is not None:
            json_body["icon"] = icon
        elif title is not None:
            json_body["title"] = title
        elif notify is not None:
            json_body["notify"] = notify
        super().__init__(path=path, params=params, json = json_body)