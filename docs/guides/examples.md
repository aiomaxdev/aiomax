# Examples

Ниже — рабочие примеры для текущего API aiomax.

## 1) Echo бот

```python
import asyncio
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

@bot.on_message()
async def echo(update):
    if update.message and update.message.body and update.message.body.text:
        await bot.send_message(chat_id=update.chat_id, text=update.message.body.text)

async def main():
    await bot.start()
    await bot.start_polling()

asyncio.run(main())
```

## 2) Команда `/start`

```python
from aiomax.filters import F

@bot.on_message(F.command("start"))
async def start(update):
    await bot.send_message(chat_id=update.chat_id, text="Бот запущен")
```

## 3) Callback-кнопка

```python
from aiomax.filters import F

@bot.on_callback(F.callback.contains("confirm"))
async def on_confirm(update):
    await bot.answer_callback(
        callback_id=update.callback.callback_id,
        notification="Подтверждено"
    )
```

## 4) FSM форма

```python
from aiomax.fsm import FSMManager, MemoryStorage, StatesGroup, State

fsm = FSMManager(MemoryStorage())

class Form(StatesGroup):
    name = State()
    age = State()
```
