from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.api_enums import ApiEnums
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.user import BotInfo

class GetMe(BaseMethod):
    path = ApiEnums.ME # исправлено, чтобы путь соответствовал API
    method = RequestMethod.GET
    response_model = BotInfo

    def __init__(self):
        # никаких параметров для GetMe
        super().__init__()