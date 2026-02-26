from aiomax.client.client import MAXClient
from aiomax.types import Message

class SendMessage:
    def __init__(self, client: MAXClient):
        self.client = client

    async def call(
        self,
        chat_id: int | None = None,
        user_id: int | None = None,
        text: str = ""
    ) -> Message:
        payload = {"text": text}
        if chat_id is not None:
            payload["chat_id"] = chat_id
        elif user_id is not None:
            payload["user_id"] = user_id
        else:
            raise ValueError("Нужно указать chat_id или user_id для отправки сообщения")
        
        # ⚡ ВАЖНО: json=payload, а не params=payload
        data = await self.client.request("POST", "/messages", json=payload)
        return Message(**data)