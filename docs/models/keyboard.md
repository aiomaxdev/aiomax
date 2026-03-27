--- docs/models/keyboard.md (原始)


+++ docs/models/keyboard.md (修改后)
# Keyboard

Keyboard markup for bot messages.

## Inline Keyboard

```python
from aiomax import types

# Single button
keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[[
        types.InlineKeyboardButton(
            text="Click me",
            callback_data="button_click"
        )
    ]]
)

# Multiple buttons
keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Option 1", callback_data="opt1"),
            types.InlineKeyboardButton(text="Option 2", callback_data="opt2")
        ],
        [
            types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
        ]
    ]
)

await bot.send_message(
    chat_id=chat_id,
    text="Choose an option:",
    reply_markup=keyboard
)
```

## URL Button

```python
keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[[
        types.InlineKeyboardButton(
            text="Visit Website",
            url="https://example.com"
        )
    ]]
)
```

## Callback Query Handling

```python
@bot.on_callback_query()
async def handle_callback(callback):
    if callback.data == "opt1":
        await bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Option 1 selected!"
        )
    elif callback.data == "cancel":
        await callback.message.delete()
```

## Reply Keyboard

```python
from aiomax import types

# Simple reply keyboard
keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        ["📍 Send Location", "📞 Send Contact"],
        ["Menu", "Help"]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

await bot.send_message(
    chat_id=chat_id,
    text="Choose an option:",
    reply_markup=keyboard
)
```

## Remove Reply Keyboard

```python
from aiomax import types

keyboard = types.ReplyKeyboardRemove()

await bot.send_message(
    chat_id=chat_id,
    text="Keyboard removed",
    reply_markup=keyboard
)
```

## Force Reply

```python
from aiomax import types

force_reply = types.ForceReply()

await bot.send_message(
    chat_id=chat_id,
    text="Please reply to this message:",
    reply_markup=force_reply
)
```

## See Also

- [Button Types](../enums/buttons.md) - Available button types
- [Message](message.md) - Message object