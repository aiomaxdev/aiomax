--- docs/enums/attachments.md (原始)


+++ docs/enums/attachments.md (修改后)
# Attachment Types

Types of file attachments supported by MAX messenger.

## Media Types

```python
from aiomax.enums import MediaType

MediaType.PHOTO       # Photo image
MediaType.VIDEO       # Video file
MediaType.AUDIO       # Audio file
MediaType.DOCUMENT    # General document
MediaType.STICKER     # Sticker
MediaType.ANIMATION   # GIF animation
MediaType.VOICE       # Voice message
MediaType.VIDEO_NOTE  # Circular video note
```

## Content Types

```python
from aiomax.enums import ContentType

ContentType.TEXT          # Text message
ContentType.PHOTO         # Photo
ContentType.VIDEO         # Video
ContentType.AUDIO         # Audio
ContentType.DOCUMENT      # Document
ContentType.STICKER       # Sticker
ContentType.ANIMATION     # Animation/GIF
ContentType.VOICE         # Voice
ContentType.VIDEO_NOTE    # Video note
ContentType.CONTACT       # Contact info
ContentType.LOCATION      # Geolocation
ContentType.VENUE         # Venue info
ContentType.POLL          # Poll
ContentType.DICE          # Dice animation
ContentType.GAME          # Game
ContentType.INVOICE       # Invoice
```

## File Extensions

| Type | Extensions | Max Size |
|------|------------|----------|
| Photo | jpg, jpeg, png, gif, bmp, webp | 10 MB |
| Video | mp4, mov, avi, mkv | 50 MB |
| Audio | mp3, m4a, wav, ogg | 50 MB |
| Voice | ogg, opus | 2 MB |
| Document | Any | 50 MB |
| Sticker | webp, tgs, webm | 512 KB |
| Animation | gif, mp4 | 50 MB |

## Checking Message Content Type

```python
@bot.on_message()
async def handle(message):
    if message.photo:
        print("Photo received")
        file_id = message.photo[-1].file_id  # Highest resolution

    elif message.video:
        print("Video received")
        file_id = message.video.file_id

    elif message.document:
        print("Document received")
        file_id = message.document.file_id

    elif message.audio:
        print("Audio received")
        file_id = message.audio.file_id

    elif message.voice:
        print("Voice received")
        file_id = message.voice.file_id

    elif message.sticker:
        print("Sticker received")
        file_id = message.sticker.file_id

    elif message.animation:
        print("Animation received")
        file_id = message.animation.file_id
```

## Filtering by Content Type

```python
from aiomax import filters

# Photos only
@bot.on_message(filters.photo)
async def handle_photo(message):
    pass

# Videos only
@bot.on_message(filters.video)
async def handle_video(message):
    pass

# Documents only
@bot.on_message(filters.document)
async def handle_document(message):
    pass

# All media
@bot.on_message(filters.media)
async def handle_media(message):
    pass
```

## Sending Different Media Types

```python
# Photo
with open("photo.jpg", "rb") as f:
    await bot.send_photo(chat_id, photo=f)

# Video
with open("video.mp4", "rb") as f:
    await bot.send_video(chat_id, video=f)

# Document
with open("file.pdf", "rb") as f:
    await bot.send_document(chat_id, document=f)

# Audio
with open("song.mp3", "rb") as f:
    await bot.send_audio(chat_id, audio=f)

# Voice
with open("voice.ogg", "rb") as f:
    await bot.send_voice(chat_id, voice=f)

# Sticker
await bot.send_sticker(chat_id, sticker="STICKER_FILE_ID")

# Animation
with open("animation.gif", "rb") as f:
    await bot.send_animation(chat_id, animation=f)
```

## Media Group

```python
from aiomax import types

media = [
    types.InputMediaPhoto(media="FILE_ID_1", caption="First"),
    types.InputMediaPhoto(media="FILE_ID_2", caption="Second"),
    types.InputMediaVideo(media="FILE_ID_3", caption="Third")
]

await bot.send_media_group(chat_id=chat_id, media=media)
```

## See Also

- [Attachments](../models/attachments.md) - Working with attachments
- [Messages](../methods/messages.md) - Message methods