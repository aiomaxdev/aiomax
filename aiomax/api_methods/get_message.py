from aiomax.api_methods.base_method import BaseMethod
from typing import List, Optional

from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.message import Message
from aiomax.models.response_status import GetMessagesResponse

class GetMessage(BaseMethod):
    method = RequestMethod.GET
    response_model = Message

    def __init__(self, 
                 *, 
                 message_id: str
                 ):

        path = f"{ApiEnums.MESSAGES.value}/{message_id}"

        super().__init__(path=path)