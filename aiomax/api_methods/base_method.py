from abc import ABC
from typing import Dict, Any, Optional, Type

from pydantic import BaseModel

from aiomax.enums.request_metod import RequestMethod


class BaseMethod(ABC):
    path: str
    method: str = RequestMethod.GET
    response_model: Optional[Type[BaseModel]] = None

    def __init__(self, params:Dict[str, Any] = None, json: Dict[str, Any]=None):
        self.params: Dict[str, Any] = params or {}
        self.json: Dict[str, Any] = json or {}


    def build(self):
        path_value = self.path.value if hasattr(self.path, "value") else self.path
        return {
            "path": path_value,
            "method": self.method,
            "params": self.params or {},
            "json": self.json or {}
        }