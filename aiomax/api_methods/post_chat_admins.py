from typing import Any, Dict, List, Optional

from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.chat_action_enums import ChatAction
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import ResponseStatus
from aiomax.models.user import ChatAdmin


class PostChatAdmins(BaseMethod):
    method: str = RequestMethod.POST
    response_model = ResponseStatus

    def __init__(self, *, 
                 chat_id: int | None = None, 
                 admins: List[dict], 
                 marker: Optional[int] = None

                 ):
        if not chat_id:
            raise ValueError("Нужно передать chat_id")

        admins_objs = [ChatAdmin(**a) for a in admins]

        json_body: Dict[str, Any] = {
            "admins": [a.model_dump() for a in admins_objs]
        }

        if marker is not None:
            json_body["marker"] = marker
        path = f"{ApiEnums.CHATS.value}/{chat_id}/members/admins"
        super().__init__(path=path, json = json_body)