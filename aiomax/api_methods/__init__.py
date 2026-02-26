from aiomax.api_methods.get_updates import GetUpdates

from .get_me import GetMe
from .send_message import SendMessage

API_METHODS = {
    "get_me": GetMe,
    "send_message": SendMessage,
    "get_updates": GetUpdates,
}