from enum import Enum


class TextStyle(str, Enum):
    """
    Возможные типы разметки текста.
    """
    STRONG = "strong"
    EMPHASIZED = "emphasized"
    MONOSPACED = "monospaced"
    LINK = "link"
    STRIKETHROUGH = "strikethrough"
    UNDERLINE = "underline"
    USER_MENTION = "user_mention"
    
    