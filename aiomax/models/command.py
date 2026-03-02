from typing import Optional

from pydantic import BaseModel


class BotCommand(BaseModel):
    name: str
    description: Optional[str] = None