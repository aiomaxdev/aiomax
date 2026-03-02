import aiohttp
from typing import Any, Dict


class MAXClient:
    def __init__(self, token: str, api_url: str = "https://platform-api.max.ru"):
        self.token = token
        self.api_url = api_url
        self._session: aiohttp.ClientSession | None = None

    async def start(self):
        self._session = aiohttp.ClientSession(
            headers={
                "Authorization": self.token,
                "Content-Type": "application/json"
            }
        )

    async def close(self):
        if self._session:
            await self._session.close()

    async def request(self, method_obj):
        if not self._session:
            raise RuntimeError("ClientSession не запущен. Вызови start().")

        data = method_obj.build()
        print(data)
        async with self._session.request(
            method=data["method"],
            url=f"{self.api_url}/{data['path']}",
            params=data.get("params"),
            json = data.get("json")
        ) as response:
            return await response.json()