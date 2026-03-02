# # aiomax/types/bot_info.py
# from typing import Optional, List
# from pydantic import BaseModel, Field

# class BotCommand(BaseModel):
#     name: str
#     description: Optional[str] = None

# class BotInfo(BaseModel):
#     id: int = Field(alias="user_id")          # user_id из API → id в модели
#     first_name: str
#     last_name: Optional[str] = None
#     username: Optional[str] = None
#     is_bot: bool
#     last_activity_time: Optional[int] = None
#     name: Optional[str] = None                # устаревшее
#     description: Optional[str] = None
#     avatar_url: Optional[str] = None
#     full_avatar_url: Optional[str] = None
#     commands: Optional[List[BotCommand]] = None

#     model_config = {
#         "populate_by_name": True               # позволяет создавать объект по ключам id или user_id
#     }