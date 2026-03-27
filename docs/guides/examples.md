# Examples

## Echo Bot

```python
from aiomax import Bot

bot = Bot(token="YOUR_TOKEN")

@bot.on_message()
async def echo(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=message.text
    )

async def main():
    await bot.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Command Bot

```python
from aiomax import Bot, filters

bot = Bot(token="YOUR_TOKEN")

@bot.on_message(filters.command("start"))
async def cmd_start(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Welcome! Use /help for commands."
    )

@bot.on_message(filters.command("help"))
async def cmd_help(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="/start - Start the bot\n/help - Show this help"
    )

async def main():
    await bot.start_polling()

asyncio.run(main())
```

## Callback Query Bot

```python
from aiomax import Bot, types

bot = Bot(token="YOUR_TOKEN")

@bot.on_message(filters.command("menu"))
async def show_menu(message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Option 1",
                callback_data="opt1"
            ),
            types.InlineKeyboardButton(
                text="Option 2",
                callback_data="opt2"
            )
        ]]
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Choose an option:",
        reply_markup=keyboard
    )

@bot.on_callback_query()
async def handle_callback(callback):
    await bot.answer_callback_query(
        callback_query_id=callback.id,
        text=f"You selected: {callback.data}"
    )
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f"Selected: {callback.data}"
    )

async def main():
    await bot.start_polling()

asyncio.run(main())
```

## FSM Conversation Bot

```python
from aiomax import Bot, FSM, State, filters

bot = Bot(token="YOUR_TOKEN")
fsm = FSM()

class FormState(State):
    name = "name"
    age = "age"

@bot.on_message(filters.command("form"))
async def start_form(message):
    await fsm.set_state(message.from_user.id, FormState.name)
    await bot.send_message(
        chat_id=message.chat.id,
        text="What is your name?"
    )

@bot.on_message(state=FormState.name)
async def process_name(message):
    await fsm.update_data(message.from_user.id, {"name": message.text})
    await fsm.set_state(message.from_user.id, FormState.age)
    await bot.send_message(
        chat_id=message.chat.id,
        text="How old are you?"
    )

@bot.on_message(state=FormState.age)
async def process_age(message):
    data = await fsm.get_data(message.from_user.id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Name: {data['name']}, Age: {message.text}"
    )
    await fsm.reset_state(message.from_user.id)

async def main():
    await bot.start_polling()

asyncio.run(main())
```

## See Also

- [Quick Start](quickstart.md) - Getting started
- [Polling](polling.md) - Long polling setup
- [Webhook](webhook.md) - Webhook configuration