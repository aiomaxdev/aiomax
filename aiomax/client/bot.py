from typing import List, Optional, Callable, Awaitable, Any
import asyncio
from aiohttp import web

from aiomax.api_methods.delete_bot_from_chat import DeleteBotFromChat
from aiomax.api_methods.delete_chat_by_chat_id import DeleteChatById
from aiomax.api_methods.delete_member_from_chat import DeleteMemberFromChat
from aiomax.api_methods.delete_message import DeleteMessage
from aiomax.api_methods.delete_permissions_from_chat import DeletePermissionsFromChat
from aiomax.api_methods.delete_pin_message import DeletePinMessage
from aiomax.api_methods.get_chat_admins import GetAdminsFromChats
from aiomax.api_methods.get_chat_info_by_chat_id import GetChatInfoById
from aiomax.api_methods.get_chat_members import GetMembersFromChats
from aiomax.api_methods.get_chats import GetChats
from aiomax.api_methods.get_me_from_chats import GetMeFromChats
from aiomax.api_methods.get_message import GetMessage
from aiomax.api_methods.get_pinned_message import GetPinnedMessage
from aiomax.api_methods.get_updates import GetUpdates
from aiomax.api_methods.patch_chat_info_by_chat_id import PatchChatInfoById
from aiomax.api_methods.post_add_members_to_chat import PostChatMembers
from aiomax.api_methods.post_chat_actions import SendAction
from aiomax.api_methods.post_chat_admins import PostChatAdmins
from aiomax.api_methods.put_message import EditMessage
from aiomax.api_methods.put_pin_message_to_chat import PutPinMessage
from aiomax.api_methods.send_message import SendMessage
from aiomax.client.client import MAXClient
from aiomax.api_methods.get_messages import GetMessages
from aiomax.api_methods.get_me import GetMe
from aiomax.models.message import Message
from aiomax.models.response_status import GetChatMemberResponse, MessageSendResponse, ResponseStatus
from aiomax.models.user import BotInfo, ChatMember
from aiomax.models.chat import Chat, Chats
from aiomax.models.update import Update
from aiomax.dispatcher import Dispatcher
from aiomax.enums.update_type import UpdateTypeEnum
from aiomax.api_methods.webhook_methods.get_subscriptions import GetSubscriptions
from aiomax.api_methods.webhook_methods.set_subscription import SetSubscription
from aiomax.api_methods.webhook_methods.delete_subscription import DeleteSubscription
from aiomax.models.webhook import SubscriptionsResponse, SubscriptionResponse


class Bot:
    def __init__(self, token: str):
        self.client = MAXClient(token)
        self._marker: int | None = None
        self._is_running = False
        self.dispatcher = Dispatcher()
        self._webhook_app: Optional[web.Application] = None
        self._webhook_runner: Optional[web.AppRunner] = None

    async def start(self):
        await self.client.start()

    async def close(self):
        await self.stop_polling()
        await self.stop_webhook()
        await self.client.close()

    async def __call__(self, method):
        return await self.client.request(method)

    # сахарок
    async def get_me(self) -> BotInfo:
        return await self(GetMe())

    async def get_messages(self, **kwargs):
        return await self(GetMessages(**kwargs))

    async def get_updates(self, **kwargs):
        return await self(GetUpdates(**kwargs))

    async def get_chats(self, **kwargs) ->Chats:
        return await self(GetChats(**kwargs))

    async def get_chat_info_by_chat_id(self, **kwargs) -> Chat:
        return await self(GetChatInfoById(**kwargs))

    async def patch_chat_info_by_chat_id(self, **kwargs) -> Chat:
        return await self(PatchChatInfoById(**kwargs))

    async def delete_chat_by_chat_id(self, **kwargs)->ResponseStatus:
        return await self(DeleteChatById(**kwargs))

    async def send_message(self, **kwargs) -> MessageSendResponse:
        return await self(SendMessage(**kwargs))

    async def send_action(self, **kwargs)->ResponseStatus:
        return await self(SendAction(**kwargs))

    async def get_pinned_message(self, **kwargs) ->Message:
        return await self(GetPinnedMessage(**kwargs))

    async def pin_message(self, **kwargs) ->ResponseStatus:
        return await self(PutPinMessage(**kwargs))

    async def unpin_message(self, **kwargs) ->ResponseStatus:
        return await self(DeletePinMessage(**kwargs))

    async def get_me_from_chat(self, **kwargs) -> ChatMember:
        return await self(GetMeFromChats(**kwargs))

    async def delete_bot_from_chat(self, **kwargs) -> ResponseStatus:
        return await self(DeleteBotFromChat(**kwargs))

    async def get_admins_from_chat(self, **kwargs) -> GetChatMemberResponse:
        return await self(GetAdminsFromChats(**kwargs))

    async def add_admins_to_chat(self, **kwargs) -> ResponseStatus:
        return await self(PostChatAdmins(**kwargs))

    async def delete_permissions_from_chat(self, **kwargs) -> ResponseStatus:
        return await self(DeletePermissionsFromChat(**kwargs))

    async def get_members_from_chat(self, **kwargs) -> GetChatMemberResponse:
        return await self(GetMembersFromChats(**kwargs))

    async def add_members_to_chat(self, **kwargs):
        return await self(PostChatMembers(**kwargs))

    async def delete_members_from_chat(self, **kwargs) -> ResponseStatus:
        return await self(DeleteMemberFromChat(**kwargs))

    async def edit_message(self, **kwargs) -> ResponseStatus:
        return await self(EditMessage(**kwargs))

    async def delete_message(self, **kwargs) -> ResponseStatus:
        return await self(DeleteMessage(**kwargs))

    async def get_message(self, **kwargs) -> Message:
        return await self(GetMessage(**kwargs))

    # Webhook методы
    async def get_subscriptions(self) -> SubscriptionsResponse:
        """Получение списка подписок на Webhook"""
        return await self(GetSubscriptions())

    async def set_subscription(
        self,
        url: str,
        update_types: Optional[List[str]] = None,
        secret: Optional[str] = None
    ) -> SubscriptionResponse:
        """Создание подписки на Webhook"""
        return await self(SetSubscription(url=url, update_types=update_types, secret=secret))

    async def delete_subscription(self, url: str) -> SubscriptionResponse:
        """Отписка от Webhook"""
        return await self(DeleteSubscription(url=url))

    # Polling с диспетчеризацией
    async def start_polling(self, *, limit:int =100, timeout: int = 30, types: List[str]| None =None):
        """Запуск long polling с автоматической диспетчеризацией обновлений"""
        self._is_running = True
        while self._is_running:
            try:
                response = await self.get_updates(
                    marker = self._marker,
                    limit = limit,
                    timeout = timeout,
                    types = types
                )
                updates = response.get("updates",[])
                self._marker = response.get("marker")

                for update_data in updates:
                    await self.dispatcher.dispatch(update_data)
            except Exception as e:
                print(f"Polling error: {e}")
                await asyncio.sleep(5)  

    async def stop_polling(self):
        """Остановка polling"""
        self._is_running = False

    # Обработчики событий (декораторы)
    def on_message(self, *filters, **kwargs):
        """
        Декоратор для регистрации обработчика сообщений.

        Args:
            *filters: Фильтры для применения к обработчику

        Example:
            @bot.on_message(F.text.contains('привет'))
            async def handle_hello(update):
                ...

            @bot.on_message()  # без фильтров - ловит все сообщения
            async def handle_all(update):
                ...
        """
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Callable:
            return self.dispatcher.register_handler(
                UpdateTypeEnum.MESSAGE_CREATED,
                callback,
                list(filters)
            )
        return decorator

    def on_callback(self, *filters, **kwargs):
        """
        Декоратор для регистрации обработчика callback.

        Args:
            *filters: Фильтры для применения к обработчику
        """
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Callable:
            return self.dispatcher.register_handler(
                UpdateTypeEnum.MESSAGE_CALLBACK,
                callback,
                list(filters)
            )
        return decorator

    def on_bot_started(self, *filters, **kwargs):
        """Декоратор для регистрации обработчика старта бота"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Callable:
            return self.dispatcher.register_handler(
                UpdateTypeEnum.BOT_STARTED,
                callback,
                list(filters)
            )
        return decorator

    def on_message_edited(self, *filters, **kwargs):
        """Декоратор для регистрации обработчика редактирования сообщения"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Callable:
            return self.dispatcher.register_handler(
                UpdateTypeEnum.MESSAGE_EDITED,
                callback,
                list(filters)
            )
        return decorator

    def on_message_removed(self, *filters, **kwargs):
        """Декоратор для регистрации обработчика удаления сообщения"""
        def decorator(callback: Callable[[Update], Awaitable[Any]]) -> Callable:
            return self.dispatcher.register_handler(
                UpdateTypeEnum.MESSAGE_REMOVED,
                callback,
                list(filters)
            )
        return decorator

    def register_handler(
        self,
        update_type: UpdateTypeEnum | str,
        callback: Callable[[Update], Awaitable[Any]]
    ):
        """Регистрация обработчика для конкретного типа обновления"""
        return self.dispatcher.register_handler(update_type, callback)

    # Webhook сервер
    async def start_webhook(
        self,
        *,
        host: str = "0.0.0.0",
        port: int = 8080,
        path: str = "/webhook",
        webhook_url: Optional[str] = None,
        secret: Optional[str] = None,
    ):
        """Запуск webhook сервера"""

        self._webhook_app = web.Application()
        self._webhook_app.router.add_post(path, self._webhook_handler)

        self._webhook_runner = web.AppRunner(self._webhook_app)
        await self._webhook_runner.setup()

        site = web.TCPSite(self._webhook_runner, host, port)
        await site.start()

        print(f"Webhook server started at http://{host}:{port}{path}")

        # если пользователь передал URL — регистрируем webhook
        if webhook_url:
            await self.set_subscription(
                url=webhook_url,
                secret=secret
            )

    async def stop_webhook(self):
        """Остановка webhook сервера"""
        if self._webhook_runner:
            await self._webhook_runner.cleanup()
            self._webhook_runner = None
            self._webhook_app = None

    async def _webhook_handler(self, request: web.Request) -> web.Response:
        """Обработчик входящих webhook запросов"""
        try:
            # Проверяем секрет если указан
            secret = request.headers.get("X-Max-Bot-Api-Secret")
            # Здесь можно добавить проверку секрета если он был установлен

            data = await request.json()

            # Обрабатываем обновление через диспетчер
            await self.dispatcher.dispatch(data)

            return web.json_response({"status": "ok"})
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return web.json_response({"status": "error"}, status=500)