
import enum


class ChatStatus(str, enum):

    ACTIVE = "active"
    REMOVED = "removed"
    LEFT = "left"
    CLOSED = "closed" 