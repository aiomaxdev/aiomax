# Installation

## Requirements

- Python 3.8+
- aiohttp

## Installation

```bash
pip install aiomax
```

## Optional Dependencies

For faster JSON parsing:

```bash
pip install aiomax[ujson]
```

## Verification

```python
import aiomax
print(aiomax.__version__)
```