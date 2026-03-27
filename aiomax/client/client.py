import aiohttp
from typing import Any, Dict

class AiomaxAPIError(Exception):
    def __init__(self, code: str, message: str, raw: dict):
        self.code = code
        self.message = message
        self.raw = raw
        super().__init__(f"{code}: {message}")

class MAXClient:
    def __init__(self, token: str, api_url: str = "https://platform-api.max.ru"):
        self.token = token
        self.api_url = api_url
        self._session: aiohttp.ClientSession | None = None

    async def start(self):
        timeout = aiohttp.ClientTimeout(total=30)

        self._session = aiohttp.ClientSession(
            timeout=timeout,
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

        async with self._session.request(
            method=data["method"],
            url=f"{self.api_url}/{data['path']}",
            
            params=data.get("params"),
            json = data.get("json")
        ) as response:
            print(data)
            raw =  await response.json()
            if response.status >= 400:
            # если API вернул код и сообщение, создаём AiomaxAPIError
                if isinstance(raw, dict) and "code" in raw and "message" in raw:
                    raise AiomaxAPIError(code=raw["code"], message=raw["message"], raw=raw)
                # иначе просто RuntimeError
                raise RuntimeError(raw)
            if method_obj.response_model:
                return method_obj.response_model.model_validate(raw)
            return raw