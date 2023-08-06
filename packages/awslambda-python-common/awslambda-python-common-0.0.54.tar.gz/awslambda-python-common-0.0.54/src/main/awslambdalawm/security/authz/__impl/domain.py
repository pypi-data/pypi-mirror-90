from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union, Dict

class Effect(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

class PolicyType(Enum):
    SUBJECT = "SUBJECT"
    RESOURCE = "RESOURCE"

@dataclass
class Rule:
    name:str
    effect:Effect
    actions:List[str]

@dataclass
class ResourcePolicyRule(Rule):
    subjects:List[str]
    conditions:List[str] = field(default_factory=list)
    obligations:List[str] = field(default_factory=list)

@dataclass
class SubjectPolicyRule(Rule):
    resources:List[str]
    conditions:List[str] = field(default_factory=list)
    obligations:List[str] = field(default_factory=list)

@dataclass
class Policy:
    name:str
    entityUri:str
    policyType:PolicyType
    rules:List[Union[SubjectPolicyRule,ResourcePolicyRule]]

@dataclass(unsafe_hash=True)
class ResourceOperation:
    action:str
    resourceUri:str

@dataclass
class PdpRequest:
    subjectUris:List[str]
    resourceOperations:List[ResourceOperation]
    conditionsContext:Dict = field(default_factory=dict)

@dataclass
class PdpResponse:
    effect:Effect
    obligations:List[str]