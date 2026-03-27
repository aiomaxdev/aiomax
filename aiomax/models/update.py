from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from aiomax.models.message import Message
from aiomax.models.user import User
from aiomax.enums.update_type import UpdateTypeEnum


class Callback(BaseModel):
    callback_id: str
    payload: Optional[str] = None 
class Update(BaseModel):
    """Модель обновления от MAX API"""
    type: UpdateTypeEnum = Field(..., alias="update_type")
    timestamp: int
    message: Optional[Message] = None
    callback: Optional[Callback] = None 
    user: Optional[User] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    message_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = Field(default=None, exclude=True)

    class Config:
        populate_by_name = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Update":
        """Создание Update из сырого словаря"""
        raw_data = data.copy()
        update_type = raw_data.pop("update_type", raw_data.pop("type", None))

        # Извлекаем общие поля
        timestamp = raw_data.pop("timestamp", 0)
        chat_id = raw_data.pop("chat_id", None)
        user_id = raw_data.pop("user_id", None)
        message_id = raw_data.pop("message_id", None)

        # Пытаемся распарсить сообщение если есть
        message = None
        if "message" in raw_data and raw_data["message"]:
            try:
                message = Message.model_validate(raw_data["message"])
            except Exception:
                pass
        callback = None
        if "callback" in raw_data and raw_data["callback"]:
            try:
                callback = Callback.model_validate(raw_data["callback"])
            except Exception:
                pass

        # Пытаемся распарсить пользователя если есть
        user = None
        if "user" in raw_data and raw_data["user"]:
            try:
                user = User.model_validate(raw_data["user"])
            except Exception:
                pass

        return cls(
            type=UpdateTypeEnum(update_type) if isinstance(update_type, str) else update_type,
            timestamp=timestamp,
            message=message,
            user=user,
            callback=callback,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
            raw=raw_data
        )