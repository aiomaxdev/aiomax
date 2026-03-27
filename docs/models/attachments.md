--- docs/models/attachments.md (原始)


+++ docs/models/attachments.md (修改后)
# Attachments

Working with file attachments in MAX messenger.

## Photo

```python
# Send photo from file
with open("photo.jpg", "rb") as f:
    await bot.send_photo(chat_id=chat_id, photo=f)

# Send photo by file_id
await bot.send_photo(chat_id=chat_id, photo="FILE_ID")

# Send photo by URL
await bot.send_photo(
    chat_id=chat_id,
    photo="https://example.com/photo.jpg"
)

# With caption
await bot.send_photo(
    chat_id=chat_id,
    photo="FILE_ID",
    caption="Beautiful photo!",
    parse_mode="HTML"
)
```

## Document

```python
# Send document
with open("document.pdf", "rb") as f:
    await bot.send_document(
        chat_id=chat_id,
        document=f,
        caption="Here's the document"
    )
```

## Video

```python
# Send video
with open("video.mp4", "rb") as f:
    await bot.send_video(
        chat_id=chat_id,
        video=f,
        duration=60,
        caption="Check this out!"
    )
```

## Audio

```python
# Send audio
with open("audio.mp3", "rb") as f:
    await bot.send_audio(
        chat_id=chat_id,
        audio=f,
        title="Song Title",
        performer="Artist"
    )
```

## Voice

```python
# Send voice message
with open("voice.ogg", "rb") as f:
    await bot.send_voice(
        chat_id=chat_id,
        voice=f,
        duration=30
    )
```

## Sticker

```python
# Send sticker
await bot.send_sticker(
    chat_id=chat_id,
    sticker="STICKER_FILE_ID"
)
```

## Animation (GIF)

```python
# Send animation
with open("animation.gif", "rb") as f:
    await bot.send_animation(
        chat_id=chat_id,
        animation=f,
        caption="Funny GIF!"
    )
```

## Location

```python
# Send location
await bot.send_location(
    chat_id=chat_id,
    latitude=55.7558,
    longitude=37.6173
)
```

## Contact

```python
# Send contact
await bot.send_contact(
    chat_id=chat_id,
    phone_number="+1234567890",
    first_name="John",
    last_name="Doe"
)
```

## Venue

```python
# Send venue
await bot.send_venue(
    chat_id=chat_id,
    latitude=55.7558,
    longitude=37.6173,
    title="Red Square",
    address="Moscow, Russia"
)
```

## Poll

```python
# Send regular poll
await bot.send_poll(
    chat_id=chat_id,
    question="What's your favorite color?",
    options=["Red", "Green", "Blue"],
    is_anonymous=False
)

# Send quiz poll
await bot.send_poll(
    chat_id=chat_id,
    question="Capital of France?",
    options=["London", "Paris", "Berlin"],
    type="quiz",
    correct_option_id=1
)
```

## File Operations

```python
# Get file
file = await bot.get_file(file_id="FILE_ID")

# Download file
await file.download("downloads/")

# Get file path
file_path = file.file_path
```

## See Also

- [Attachment Types](../enums/attachments.md) - Available attachment types
- [Message](message.md) - Message object