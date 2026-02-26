# aiomax/client/client.py
import aiohttp
from typing import Any, Dict, Optional

class MAXClient:
    def __init__(self, token: str, api_url: str = "https://platform-api.max.ru"):
        self.token = token
        self.api_url = api_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": self.token,
                    "Content-Type": "application/json"
                }
            )
        return self._session

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None  # ⚡ добавили поддержку json
    ) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.api_url}{path}"
        async with session.request(method.upper(), url, params=params, json=json) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()