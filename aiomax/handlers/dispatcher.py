from typing import Any, Awaitable, Callable, Dict, List, Optional
from aiomax.handlers.router import Router
from aiomax.handlers.fsm import FSMContext, BaseStorage, MemoryStorage
from aiomax.handlers.middleware import Middleware
from aiomax.client.bot import Bot


class Dispatcher:
    """
    Диспетчер для обработки событий бота.
    Аналог Dispatcher в aiogram.
    
    Диспетчер объединяет роутеры, middleware и FSM контекст,
    предоставляя единый интерфейс для обработки событий.
    
    Пример использования:
        from aiomax import Bot, Dispatcher, Router, F
        
        bot = Bot("TOKEN")
        dp = Dispatcher()
        router = Router()
        
        @router.on_message(F.Command("/start"))
        async def start_handler(event, context):
            await bot.send_message(
                chat_id=event["message"]["recipient"]["chat_id"],
                text="Привет! Я бот."
            )
        
        dp.include_router(router)
        
        async def main():
            await bot.start()
            await dp.start_polling(bot)
        
        asyncio.run(main())
    """
    
    def __init__(self, storage: Optional[BaseStorage] = None):
        self._routers: List[Router] = []
        self._middleware: List[Middleware] = []
        self.storage = storage or MemoryStorage()
        self._context: Dict[str, Any] = {}
    
    def include_router(self, router: Router) -> None:
        """Подключить роутер к диспетчеру"""
        self._routers.append(router)
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Добавить middleware"""
        self._middleware.append(middleware)
    
    async def _build_middleware_chain(
        self,
        handler: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]:
        """Построить цепочку middleware"""
        async def wrapped(event: Dict[str, Any], context: Dict[str, Any]) -> Any:
            # Создаём цепочку вызовов middleware
            chain = handler
            for mw in reversed(self._middleware):
                chain = self._wrap_middleware(mw, chain)
            return await chain(event, context)
        
        return wrapped
    
    def _wrap_middleware(
        self,
        middleware: Middleware,
        inner: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]
    ) -> Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[Any]]:
        """Обёртка middleware"""
        async def call_with_middleware(event: Dict[str, Any], context: Dict[str, Any]) -> Any:
            async def call_next(e: Dict[str, Any], c: Dict[str, Any]) -> Any:
                return await inner(e, c)
            return await middleware(event, context, call_next)
        
        return call_with_middleware
    
    async def process_event(self, bot: Bot, event: Dict[str, Any]) -> bool:
        """
        Обработать событие через все роутеры.
        Возвращает True, если событие было обработано.
        """
        # Получаем данные пользователя для FSM
        user_id = event.get("message", {}).get("sender", {}).get("user_id")
        chat_id = event.get("message", {}).get("recipient", {}).get("chat_id")
        
        if user_id:
            fsm = FSMContext(self.storage, user_id, chat_id)
            state = await fsm.get_state()
            
            # Добавляем FSM контекст в общий контекст
            context = {
                "bot": bot,
                "fsm": fsm,
                "state": state,
                **self._context
            }
        else:
            context = {
                "bot": bot,
                **self._context
            }
        
        # Проходим по всем роутерам
        for router in self._routers:
            # Создаём цепочку обработки с middleware
            async def handle(e: Dict[str, Any], c: Dict[str, Any]) -> bool:
                return await router.process_event(e, c)
            
            chain = await self._build_middleware_chain(handle)
            
            if await chain(event, context):
                return True
        
        return False
    
    async def start_polling(self, bot: Bot, limit: int = 100, timeout: int = 30, types: Optional[List[str]] = None) -> None:
        """
        Запустить polling событий.
        
        Args:
            bot: Экземпляр бота
            limit: Максимальное количество обновлений за запрос
            timeout: Таймаут long polling
            types: Список типов событий для получения
        """
        print("Запуск polling...")
        
        async for update in bot.start_polling(limit=limit, timeout=timeout, types=types):
            try:
                await self.process_event(bot, update)
            except Exception as e:
                print(f"Ошибка при обработке события: {e}")
                # Здесь можно добавить логирование
    
    async def feed_update(self, bot: Bot, update: Dict[str, Any]) -> bool:
        """
        Передать обновление на обработку.
        Полезно для webhook режима.
        """
        return await self.process_event(bot, update)
