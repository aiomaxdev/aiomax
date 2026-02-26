from typing import Optional, Dict, Any
from pydantic import BaseModel
from aiomax.types.message import Message


class Update(BaseModel):
    update_type: str
    timestamp: int
    message: Optional[Message] = None
    user_locale: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None  # сохраняем все остальное "на будущее"

    class Config:
        arbitrary_types_allowed = True  # если нужны нестандартные типы