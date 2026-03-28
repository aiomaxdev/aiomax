# Filters

Фильтры определяют, какие обновления попадут в обработчик.

В aiomax рекомендуется использовать фабрику `F` из `aiomax.filters`.

## Быстрый старт

```python
from aiomax.filters import F

@bot.on_message(F.command("start"))
async def start_cmd(update):
    ...

@bot.on_message(F.text.contains("привет"))
async def hello(update):
    ...

@bot.on_callback(F.callback.contains("confirm"))
async def cb(update):
    ...
```

## Доступные фильтры

```python
from aiomax.filters import F

F.text.exact("hello")
F.text.contains("hel")
F.text.startswith("/start")
F.text.endswith("!")
F.text.regex(r"^/ban\\s+\\d+$")

F.command("start")
F.chat(-100123456)
F.user(111, 222)
F.callback.data("approve")
F.callback.contains("approve")
F.content("image")  # text/image/video/audio/file/contact/location
```

## Комбинация фильтров

```python
from aiomax.filters import F

@bot.on_message(F.command("start") | F.command("help"))
async def start_or_help(update):
    ...

@bot.on_message(F.text.contains("urgent") & ~F.user(999999))
async def not_blocked(update):
    ...
```
