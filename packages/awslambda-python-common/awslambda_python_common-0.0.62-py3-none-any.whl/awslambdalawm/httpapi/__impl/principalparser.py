import os
from dataclasses import dataclass, field
from typing import Dict, ClassVar, List
import jwt
import awslambdalawm.security as security

class PrincipalParser:

    def __init__(self, 
            jwtIdTokenSubjectIdField:str,
            jwtIdTokenTenantField:str,
            jwtIdTokenRolesField:str,
            jwtSystemAccessTokenScopePrefix:str
    ):
        self.__jwtIdTokenSubjectIdField = jwtIdTokenSubjectIdField
        self.__jwtIdTokenTenantField = jwtIdTokenTenantField
        self.__jwtIdTokenRolesField = jwtIdTokenRolesField
        self.__jwtSystemAccessTokenScopePrefix = jwtSystemAccessTokenScopePrefix

    def getPrincipalFromEvent(self, event:Dict) -> security.Principal:
        if "headers" not in event or not "authorization" in event["headers"]:
            return None
        authorizationHeader = event["headers"]["authorization"]
        if authorizationHeader is None:
            return None
        jwtToken = authorizationHeader[len("Bearer "):]
        decodedJwt = jwt.decode(jwtToken, options={"verify_signature": False})
        tokenUse = decodedJwt["token_use"]
        if tokenUse == "id":
            clientId = decodedJwt["aud"]
            subjectType = security.Principal.SUBJECT_TYPE_USER
            subjectId = decodedJwt[self.__jwtIdTokenSubjectIdField]
            tenant = decodedJwt[self.__jwtIdTokenTenantField]
            rolesStr = decodedJwt[self.__jwtIdTokenRolesField]
            roles = rolesStr.split(",") if len(rolesStr) > 0 else []
            principal = security.Principal(
                clientId = clientId,
                subjectType = subjectType, 
                subjectId = subjectId, 
                tenant = tenant,
                token = jwtToken,
                roles = roles
            )    
            return principal    
        elif tokenUse == "access":
            subjectId = decodedJwt["sub"]
            subjectType = security.Principal.SUBJECT_TYPE_SYSTEM
            # sample valid scope: https://projectx.platform-dev/projectxb2c
            scope = decodedJwt["scope"]
            tenantPrefixSplit = scope.rsplit("/", 1)
            [prefix, tenant] = tenantPrefixSplit      
            if prefix != self.__jwtSystemAccessTokenScopePrefix:
                raise Exception("Invalid scope in token")
            principal = security.Principal(
                clientId = subjectId,
                subjectType = subjectType, 
                subjectId = subjectId, 
                tenant = tenant,
                token = jwtToken
            )
            return principal
        else:
            raise Exception(f"Invalid token use {tokenUse} encountered")
