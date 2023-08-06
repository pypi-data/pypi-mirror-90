import os
from dataclasses import dataclass, field
from typing import Dict, ClassVar, List
import jwt

@dataclass
class Principal:
    clientId:str
    subjectType:str
    subjectId:str
    tenant:str
    token:str
    roles:List[str] = field(default_factory=list)
    SUBJECT_TYPE_USER:ClassVar[str] = "user"
    SUBJECT_TYPE_SYSTEM:ClassVar[str] = "system"
    DELEGATED_ACCESS:ClassVar[str] = "delegated-access"