# Button Types

Types of buttons available for keyboards.

## Inline Keyboard Buttons

Buttons that appear below the message.

```python
from aiomax import types

# Callback button
button = types.InlineKeyboardButton(
    text="Click me",
    callback_data="button_click"
)

# URL button
button = types.InlineKeyboardButton(
    text="Visit Website",
    url="https://example.com"
)

# Login button
button = types.InlineKeyboardButton(
    text="Login",
    login_url=types.LoginUrl(url="https://example.com/login")
)

# Switch to inline button
button = types.InlineKeyboardButton(
    text="Search",
    switch_inline_query="query"
)

# Switch to current chat inline button
button = types.InlineKeyboardButton(
    text="Share",
    switch_inline_query_current_chat="text"
)

# Copy text button
button = types.InlineKeyboardButton(
    text="Copy Code",
    copy_text="print('Hello')"
)

# Web app button
button = types.InlineKeyboardButton(
    text="Open App",
    web_app=types.WebAppInfo(url="https://example.com/app")
)
```

## Reply Keyboard Buttons

Buttons that replace the standard keyboard.

```python
from aiomax import types

# Simple text button
button = types.KeyboardButton(text="Send Location")

# Request location button
button = types.KeyboardButton(
    text="📍 Send Location",
    request_location=True
)

# Request contact button
button = types.KeyboardButton(
    text="📞 Send Contact",
    request_contact=True
)

# Request poll button
button = types.KeyboardButton(
    text="Create Poll",
    request_poll=types.KeyboardButtonPollType(type="quiz")
)

# Web app button (reply keyboard)
button = types.KeyboardButton(
    text="Open Menu",
    web_app=types.WebAppInfo(url="https://example.com/menu")
)
```

## Creating Keyboards

### Inline Keyboard

```python
from aiomax import types

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
```

### Reply Keyboard

```python
from aiomax import types

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        ["Menu", "Help"],
        [
            types.KeyboardButton(text="📍 Location", request_location=True),
            types.KeyboardButton(text="📞 Contact", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
```

## Button Actions

### Handling Callback Buttons

```python
@bot.on_callback_query()
async def handle_callback(callback):
    data = callback.data

    if data == "opt1":
        await bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Option 1 selected!"
        )
    elif data == "cancel":
        await callback.message.delete()
```

### Handling Reply Buttons

```python
from aiomax import filters

@bot.on_message(filters.text)
async def handle_reply(message):
    if message.text == "Menu":
        await show_menu(message)
    elif message.text == "Help":
        await show_help(message)
```

## See Also

- [Keyboard](../models/keyboard.md) - Keyboard markup
- [Examples](../guides/examples.md) - Bot examples