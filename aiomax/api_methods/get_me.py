from aiomax.client.client import MAXClient
from aiomax.types.bot_info import BotInfo

class GetMe:
    def __init__(self, client: MAXClient):
        self.client = client

    async def call(self) -> BotInfo:
        data = await self.client.request("GET", "/me")
        return BotInfo(**data)