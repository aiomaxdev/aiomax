"""
AioMax - современный асинхронный фреймворк для создания ботов.

Базовые импорты:
    from aiomax import Bot, Update, Message, Chat, User, UpdateTypeEnum

Для расширенной функциональности используйте отдельные модули:
    from aiomax.dispatcher import Dispatcher, Handler
    from aiomax.filters import F, TextFilter, CommandFilter
    from aiomax.fsm import FSMManager, MemoryStorage, StatesGroup
"""
from .client.bot import Bot
from .enums.update_type import UpdateTypeEnum
from .models.update import Update
from .models.message import Message
from .models.chat import Chat
from .models.user import User

__version__ = "1.2.0"
__all__ = [
    # Bot client
    "Bot",
    # Enums
    "UpdateTypeEnum",
    # Core models
    "Update",
    "Message",
    "Chat",
    "User",
]