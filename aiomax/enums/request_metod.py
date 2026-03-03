from enum import Enum
class RequestMethod(str, Enum):
    
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"