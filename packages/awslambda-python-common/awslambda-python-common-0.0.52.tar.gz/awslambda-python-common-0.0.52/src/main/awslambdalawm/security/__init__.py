from dataclasses import dataclass as __dataclass
from awslambdalawm.security.core.__impl import PermissionsHelper
import awslambdalawm.security.core.__impl.context as context
from awslambdalawm.security.core.__impl.domain import Principal
from awslambdalawm.security.authz.__impl.domain import ResourceOperation
from awslambdalawm.security.authz.__impl.domain import Policy, Effect, PolicyType, SubjectPolicyRule, ResourcePolicyRule
from awslambdalawm.security.authz.__impl.exception import AccessDeniedException
from awslambdalawm.security.authz.__impl.pep import Pep
from awslambdalawm.security.authz.__impl.pdprepo import PdpRepo as __PdpRepo
from awslambdalawm.security.authz.__impl.pdpservice import PdpService

@__dataclass
class __Instances:
    pdpService:PdpService=None,
    pep:Pep=None

__INSTANCES = __Instances()

def configure(
    policiesTableName:str, 
    policiesTableEntityUriFieldName:str = "entityUri",
    policiesTablePolicyTypeFieldName:str = "policyType",
    policiesKeyPrefix:str = "POLICY#"
) -> None:
    pdpRepo = __PdpRepo(
        policiesTableName,
        policiesTableEntityUriFieldName,
        policiesTablePolicyTypeFieldName,
        policiesKeyPrefix
    )
    __INSTANCES.pdpService = PdpService(pdpRepo)
    __INSTANCES.pep = Pep(__INSTANCES.pdpService)

def pep() -> Pep:
    return __INSTANCES.pep

def pdpService():
    return __INSTANCES.pdpService