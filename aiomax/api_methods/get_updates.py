from typing import List, Optional
from aiomax.client.client import MAXClient
from aiomax.types.update import Update


class GetUpdates:
    def __init__(self, client: MAXClient):
        self.client = client

    async def call(
        self,
        offset: Optional[int] = None,
        limit: int = 100,
        timeout: int = 30
    ) -> List[Update]:
        params = {
            "limit": limit,
            "timeout": timeout,
        }
        if offset is not None:
            params["offset"] = offset

        data = await self.client.request(
            "GET",
            "/updates",
            params=params
        )

        # Берем список апдейтов из ключа "updates"
        updates_list = data.get("updates", [])

        # Возвращаем список объектов Update
        return [Update(**item) for item in updates_list]