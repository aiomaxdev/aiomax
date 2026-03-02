from abc import ABC
from typing import Dict, Any, Optional, Type

from pydantic import BaseModel


class BaseMethod(ABC):
    path: str
    method: str = "GET"
    response_model: Optional[Type[BaseModel]] = None

    def __init__(self, params:Dict[str, Any] = None, json: Dict[str, Any]=None):
        self.params: Dict[str, Any] = params or {}
        self.json: Dict[str, Any] = json or {}


    def build(self):
        return {
            "path": self.path,
            "method": self.method,
            "params": self.params or {},
            "json": self.json or {}
        }