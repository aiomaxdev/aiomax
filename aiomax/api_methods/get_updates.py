from aiomax.api_methods.base_method import BaseMethod
from typing import Optional, List


class GetUpdates(BaseMethod):
    path = "updates"
    method = "GET"

    def __init__(
        self,
        *,
        limit: int = 100,
        timeout: int = 30,
        marker: Optional[int] = None,
        types: Optional[List[str]] = None,
    ):
        if not (1 <= limit <= 1000):
            raise ValueError("limit должен быть от 1 до 1000")
        if not (0 <= timeout <= 90):
            raise ValueError("timeout должен быть от 0 до 90")
        params = {
            "limit": limit,
            "timeout": timeout,
        }
        if marker is not None:
            params["marker"] = marker
        if types:
            params["types"] = ",".join(types)

        super().__init__(params = params)