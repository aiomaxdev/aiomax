from enum import Enum


class ChatAction(str, Enum):
    """Действия бота в чате (индикаторы активности)."""

    TYPING = "typing_on"
    SENDING_PHOTO = "sending_photo"
    SENDING_VIDEO = "sending_video"
    SENDING_AUDIO = "sending_audio"
    SENDING_FILE = "sending_file"
    MARK_SEEN = "mark_seen"