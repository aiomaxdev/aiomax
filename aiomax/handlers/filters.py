from typing import Any, Awaitable, Callable, Dict, List, Optional
from aiomax.handlers.handler import BaseFilter, EventType


class F:
    """
    Коллекция встроенных фильтров.
    Аналог F в aiogram.
    
    Пример использования:
        @router.on_message(F.Text("hello"))
        async def handle_hello(event, context):
            ...
        
        @router.on_message(F.Command("/start"))
        async def handle_start(event, context):
            ...
        
        @router.on_message(F.ChatID(-100123456789))
        async def handle_group(event, context):
            ...
    """
    
    class Text(BaseFilter):
        """Фильтр по тексту сообщения"""
        
        def __init__(self, text: Optional[str] = None, contains: Optional[str] = None, startswith: Optional[str] = None):
            self.text = text
            self.contains = contains
            self.startswith = startswith
        
        async def __call__(self, event: Dict[str, Any]) -> bool:
            message_data = event.get("message", {})
            body = message_data.get("body", {})
            text = body.get("text", "")
            
            if not text:
                return False
            
            if self.text is not None and text == self.text:
                return True
            
            if self.contains is not None and self.contains in text:
                return True
            
            if self.startswith is not None and text.startswith(self.startswith):
                return True
            
            return False
    
    class Command(BaseFilter):
        """Фильтр по команде"""
        
        def __init__(self, command: str, prefixes: List[str] = None):
            self.command = command.lstrip("/")
            self.prefixes = prefixes or ["/"]
        
        async def __call__(self, event: Dict[str, Any]) -> bool:
            message_data = event.get("message", {})
            body = message_data.get("body", {})
            text = body.get("text", "")
            
            if not text:
                return False
            
            for prefix in self.prefixes:
                if text.startswith(prefix):
                    cmd = text[len(prefix):].split()[0].split("@")[0]
                    if cmd == self.command:
                        return True
            
            return False
    
    class ChatID(BaseFilter):
        """Фильтр по ID чата"""
        
        def __init__(self, chat_id: int):
            self.chat_id = chat_id
        
        async def __call__(self, event: Dict[str, Any]) -> bool:
            message_data = event.get("message", {})
            recipient = message_data.get("recipient", {})
            event_chat_id = recipient.get("chat_id")
            
            return event_chat_id == self.chat_id
    
    class UserID(BaseFilter):
        """Фильтр по ID пользователя"""
        
        def __init__(self, user_id: int):
            self.user_id = user_id
        
        async def __call__(self, event: Dict[str, Any]) -> bool:
            message_data = event.get("message", {})
            sender = message_data.get("sender", {})
            event_user_id = sender.get("user_id")
            
            return event_user_id == self.user_id
    
    class CallbackData(BaseFilter):
        """Фильтр по данным callback"""
        
        def __init__(self, data: Optional[str] = None, contains: Optional[str] = None):
            self.data = data
            self.contains = contains
        
        async def __call__(self, event: Dict[str, Any]) -> bool:
            callback_data = event.get("callback", {}).get("data", "")
            
            if not callback_data:
                return False
            
            if self.data is not None and callback_data == self.data:
                return True
            
            if self.contains is not None and self.contains in callback_data:
                return True
            
            return False
    
    class State(BaseFilter):
        """Фильтр по состоянию FSM"""
        
        def __init__(self, state: str):
            self.state = state
        
        async def __call__(self, event: Dict[str, Any]) -> bool:
            context = event.get("context", {})
            current_state = context.get("state", "")
            
            return current_state == self.state
