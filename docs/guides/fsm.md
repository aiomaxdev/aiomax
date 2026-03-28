# Finite State Machine (FSM)

FSM в aiomax реализован через `FSMManager` и хранилище (например, `MemoryStorage`).

## Базовая настройка

```python
from aiomax.fsm import FSMManager, MemoryStorage, StatesGroup, State

fsm = FSMManager(MemoryStorage())

class Form(StatesGroup):
    name = State()
    age = State()
```

## Использование в обработчиках

```python
from aiomax.filters import F

@bot.on_message(F.command("start"))
async def start_form(update):
    user_id = update.user_id
    chat_id = update.chat_id

    await fsm.set_state(user_id, str(Form.name), chat_id)
    await bot.send_message(chat_id=chat_id, text="Как вас зовут?")

@bot.on_message()
async def form_router(update):
    user_id = update.user_id
    chat_id = update.chat_id
    text = update.message.body.text if update.message and update.message.body else ""

    state = await fsm.get_state(user_id, chat_id)

    if state == str(Form.name):
        await fsm.update_data(user_id, {"name": text}, chat_id)
        await fsm.set_state(user_id, str(Form.age), chat_id)
        await bot.send_message(chat_id=chat_id, text="Сколько вам лет?")
        return

    if state == str(Form.age):
        data = await fsm.get_data(user_id, chat_id)
        await bot.send_message(chat_id=chat_id, text=f"Имя: {data['name']}, возраст: {text}")
        await fsm.clear(user_id, chat_id)
```

## Хранилища

Сейчас в библиотеке есть `MemoryStorage`.
