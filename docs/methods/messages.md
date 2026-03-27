--- docs/methods/messages.md (原始)


+++ docs/methods/messages.md (修改后)
# Messages

Methods for sending and managing messages.

## send_message

Send a text message.

```python
await bot.send_message(
    chat_id=chat_id,
    text="Hello, World!",
    parse_mode="HTML",  # or "Markdown"
    disable_web_page_preview=True
)
```

## send_photo

Send a photo.

```python
# From file
with open("photo.jpg", "rb") as f:
    await bot.send_photo(
        chat_id=chat_id,
        photo=f,
        caption="Beautiful photo!"
    )

# By file_id or URL
await bot.send_photo(
    chat_id=chat_id,
    photo="FILE_ID_or_URL"
)
```

## send_document

Send a document.

```python
with open("document.pdf", "rb") as f:
    await bot.send_document(
        chat_id=chat_id,
        document=f,
        caption="Here's the document"
    )
```

## send_video

Send a video.

```python
with open("video.mp4", "rb") as f:
    await bot.send_video(
        chat_id=chat_id,
        video=f,
        duration=60,
        caption="Check this out!",
        supports_streaming=True
    )
```

## send_audio

Send an audio file.

```python
with open("audio.mp3", "rb") as f:
    await bot.send_audio(
        chat_id=chat_id,
        audio=f,
        title="Song Title",
        performer="Artist"
    )
```

## send_voice

Send a voice message.

```python
with open("voice.ogg", "rb") as f:
    await bot.send_voice(
        chat_id=chat_id,
        voice=f,
        duration=30
    )
```

## send_sticker

Send a sticker.

```python
await bot.send_sticker(
    chat_id=chat_id,
    sticker="STICKER_FILE_ID"
)
```

## send_animation

Send an animation (GIF).

```python
with open("animation.gif", "rb") as f:
    await bot.send_animation(
        chat_id=chat_id,
        animation=f,
        caption="Funny GIF!"
    )
```

## send_location

Send a location.

```python
await bot.send_location(
    chat_id=chat_id,
    latitude=55.7558,
    longitude=37.6173,
    horizontal_accuracy=10
)
```

## send_venue

Send a venue.

```python
await bot.send_venue(
    chat_id=chat_id,
    latitude=55.7558,
    longitude=37.6173,
    title="Red Square",
    address="Moscow, Russia"
)
```

## send_contact

Send a contact.

```python
await bot.send_contact(
    chat_id=chat_id,
    phone_number="+1234567890",
    first_name="John",
    last_name="Doe"
)
```

## send_poll

Send a poll.

```python
# Regular poll
await bot.send_poll(
    chat_id=chat_id,
    question="What's your favorite color?",
    options=["Red", "Green", "Blue"],
    is_anonymous=False,
    allows_multiple_answers=True
)

# Quiz poll
await bot.send_poll(
    chat_id=chat_id,
    question="Capital of France?",
    options=["London", "Paris", "Berlin"],
    type="quiz",
    correct_option_id=1
)
```

## edit_message_text

Edit message text.

```python
await bot.edit_message_text(
    chat_id=chat_id,
    message_id=message_id,
    text="Updated text!",
    reply_markup=new_keyboard
)

# For inline messages
await bot.edit_message_text(
    inline_message_id=inline_id,
    text="Updated!"
)
```

## edit_message_caption

Edit message caption.

```python
await bot.edit_message_caption(
    chat_id=chat_id,
    message_id=message_id,
    caption="New caption"
)
```

## edit_message_media

Edit message media.

```python
from aiomax import types

new_media = types.InputMediaPhoto(
    media="NEW_FILE_ID",
    caption="New caption"
)

await bot.edit_message_media(
    chat_id=chat_id,
    message_id=message_id,
    media=new_media
)
```

## delete_message

Delete a message.

```python
await bot.delete_message(
    chat_id=chat_id,
    message_id=message_id
)
```

## See Also

- [General Methods](general.md) - General utility methods
- [Attachments](../models/attachments.md) - Working with attachments