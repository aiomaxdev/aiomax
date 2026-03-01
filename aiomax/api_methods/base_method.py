from abc import ABC
from typing import Dict, Any


class BaseMethod(ABC):
    path: str
    method: str = "GET"

    def __init__(self, **params):
        self.params: Dict[str, Any] = params

    def build(self):
        return {
            "path": self.path,
            "method": self.method,
            "params": self.params
        }