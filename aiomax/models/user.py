from typing import List, Optional

from pydantic import BaseModel

from aiomax.models.command import BotCommand

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: bool
    last_activity_time: Optional[int] = None
    name:str # устареет скоро, следить

class UserWithPhoto(User):
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    full_avatar_url: Optional[str] = None

class BotInfo(UserWithPhoto):
    commands: Optional[List[BotCommand]] = None
