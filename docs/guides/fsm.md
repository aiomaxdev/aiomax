--- docs/guides/fsm.md (原始)


+++ docs/guides/fsm.md (修改后)
# Finite State Machine (FSM)

FSM allows you to manage conversation states in your bot.

## Basic Setup

```python
from aiomax import Bot, FSM, State

bot = Bot(token="YOUR_TOKEN")
fsm = FSM()

class MyStates(State):
    waiting_for_name = "waiting_for_name"
    waiting_for_age = "waiting_for_age"
```

## Using States

```python
@bot.on_message(filters.command("/start"))
async def start(message):
    await fsm.set_state(message.from_user.id, MyStates.waiting_for_name)
    await bot.send_message(
        chat_id=message.chat.id,
        text="What is your name?"
    )

@bot.on_message(state=MyStates.waiting_for_name)
async def get_name(message):
    await fsm.update_data(
        message.from_user.id,
        {"name": message.text}
    )
    await fsm.set_state(message.from_user.id, MyStates.waiting_for_age)
    await bot.send_message(
        chat_id=message.chat.id,
        text="How old are you?"
    )

@bot.on_message(state=MyStates.waiting_for_age)
async def get_age(message):
    data = await fsm.get_data(message.from_user.id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Name: {data['name']}, Age: {message.text}"
    )
    await fsm.reset_state(message.from_user.id)
```

## Storage Backends

### Memory Storage (default)

```python
from aiomax.storage import MemoryStorage
fsm = FSM(storage=MemoryStorage())
```

### Redis Storage

```python
from aiomax.storage import RedisStorage
fsm = FSM(storage=RedisStorage(host="localhost", port=6379))
```

## See Also

- [Handlers](handlers.md) - Working with handlers