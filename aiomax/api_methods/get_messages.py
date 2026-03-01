from aiomax.api_methods.base_method import BaseMethod


class GetMessages(BaseMethod):
    path = "messages"
    method = "GET"

    def __init__(self, *, chat_id: str = None, message_ids: list[str] = None):
        if chat_id and message_ids:
            raise ValueError("Нельзя передавать одновременно chat_id и message_ids")

        if not chat_id and not message_ids:
            raise ValueError("Нужно передать либо chat_id, либо message_ids")

        if chat_id:
            super().__init__(chat_id=chat_id)
        else:
            super().__init__(message_ids=",".join(message_ids))