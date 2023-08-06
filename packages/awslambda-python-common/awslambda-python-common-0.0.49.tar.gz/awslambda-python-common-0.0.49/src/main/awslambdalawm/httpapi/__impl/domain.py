from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    TRACE = "TRACE"

@dataclass
class Request:
    pathParams:Dict[str,str]
    queryParams:Dict[str,str]
    body:Any

@dataclass
class Response:
    statusCode:int
    responseBody:object = None