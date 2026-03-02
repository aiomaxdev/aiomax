from aiomax.api_methods.base_method import BaseMethod
from aiomax.models.user import BotInfo

class GetMe(BaseMethod):
    path = "me"  # исправлено, чтобы путь соответствовал API
    method = "GET"
    response_model = BotInfo

    def __init__(self):
        # никаких параметров для GetMe
        super().__init__()