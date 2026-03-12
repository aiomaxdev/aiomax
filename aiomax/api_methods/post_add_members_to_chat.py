from typing import Any, Dict, List, Optional
from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.response_status import AddMembersToChat



class PostChatMembers(BaseMethod):
    method: str = RequestMethod.POST
    response_model = AddMembersToChat

    def __init__(self, *, 
                 chat_id: int | None = None, 
                 user_ids: Optional[List[int]] = None, 
                 ):
        if not chat_id:
            raise ValueError("Нужно передать chat_id")

        json_body: Dict[str, Any]={}
        if user_ids is not None:
            json_body["user_ids"] = user_ids
        path = f"{ApiEnums.CHATS.value}/{chat_id}/members"
        super().__init__(path=path, json = json_body)