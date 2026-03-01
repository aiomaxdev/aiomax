from aiomax.api_methods.base_method import BaseMethod

class GetMe(BaseMethod):
    path = "me"  # исправлено, чтобы путь соответствовал API
    method = "GET"

    def __init__(self):
        # никаких параметров для GetMe
        super().__init__()