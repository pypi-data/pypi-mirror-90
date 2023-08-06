from dataclasses import dataclass as __dataclass
from aws_lambda_powertools.logging import Logger as __Logger
from awslambdalawm.httpapi.__impl.app import App as HttpApiApp
from awslambdalawm.httpapi.__impl.principalparser import PrincipalParser as __PrincipalParser
from awslambdalawm.httpapi.__impl.domain import (
    RequestMethod as HttpRequestMethod, 
    Request as HttpRequest,
    Response as HttpResponse
)

@__dataclass
class __Instances:
    httpApiApp:HttpApiApp = None

__Instances = __Instances()

def configure(
    jwtIdTokenSubjectIdField:str,
    jwtIdTokenTenantField:str,
    jwtIdTokenRolesField:str,
    jwtSystemAccessTokenScopePrefix:str,
    logger:__Logger = None
) -> None:
    principalParser = __PrincipalParser(
        jwtIdTokenSubjectIdField=jwtIdTokenSubjectIdField,
        jwtIdTokenTenantField=jwtIdTokenTenantField,
        jwtIdTokenRolesField=jwtIdTokenRolesField,
        jwtSystemAccessTokenScopePrefix=jwtSystemAccessTokenScopePrefix,
    )
    if logger is None:
        __Instances.httpApiApp = HttpApiApp(principalParser=principalParser)
    else:
        __Instances.httpApiApp = HttpApiApp(principalParser=principalParser, logger=logger) 


def httpApiApp() -> HttpApiApp:
    return __Instances.httpApiApp