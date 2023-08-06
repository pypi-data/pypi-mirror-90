import os
import inspect
import json
from datetime import date, datetime
from collections import namedtuple
from typing import Dict, Callable
from dataclasses import asdict, is_dataclass
import jwt
import dacite
from aws_lambda_powertools import Logger
from awslambdalawm.util import DatetimeUtil, ObjectUtil
from awslambdalawm.httpapi.__impl.domain import RequestMethod, Request, Response
from awslambdalawm.httpapi.__impl.principalparser import PrincipalParser
import awslambdalawm.security as security

class App:    
    __FnSpec = namedtuple("FnSpec", ("fn", "principalRequired", "requestBodyType"))  

    def __init__(self, principalParser:PrincipalParser, logger:Logger = None):
        super().__init__()
        self.__functionRegistry = {}
        self.__logger = Logger() if logger is None else logger
        self.__principalParser = principalParser

    def route(self, 
        path:str, 
        method:RequestMethod, 
        principalRequired:bool = True,
        requestBodyType:type = None
    ) -> Callable:
        def wrapper(fn):
            self.__logger.info(f"Adding to function registry: key={method.name} {path}, fn={fn}, principalRequired={principalRequired}, requestBodyType={requestBodyType}")
            self.__functionRegistry[f"{method.name} {path}"] = App.__FnSpec(fn, principalRequired, requestBodyType)     
            return fn
        return wrapper

    def handle(self, event:Dict, context:Dict) -> Dict:
        routeKey = event["routeKey"]
        self.__logger.info(f"Request for routeKey={routeKey} received")
        targetFnSpec:App.__FnSpec = self.__functionRegistry[routeKey]
        targetFn = targetFnSpec.fn
        argspec = inspect.getfullargspec(targetFn)
        targetFnArgNames = argspec[0]
        targetFnKwargs = argspec.varkw
        newKwargs = {}
        newVarargs = []
        if "event" in targetFnArgNames or not targetFnKwargs is None:
            newKwargs["event"] = event
        if "context" in targetFnArgNames or not targetFnKwargs is None:
            newKwargs["context"] = context
        # detect principal and inject if in argument list
        principal = None
        try:
            principal = self.__principalParser.getPrincipalFromEvent(event)
        except Exception as e:
            self.__logger.exception(f"Error parsing principal from request: {e}")
        security.context.setPrincipal(principal)
        if principal is None:
            self.__logger.info(f"No valid principal detected")
            if targetFnSpec.principalRequired:        
                # return error
                return(self.__generateLambdaResponse(Response(401)))
        else:
            self.__logger.info(f"Detected principal: tenant={principal.tenant}, subjectType={principal.subjectType}, subjectId={principal.subjectId}")
        if "principal" in targetFnArgNames or not targetFnKwargs is None:
            self.__logger.info(f"Injecting principal into route handler")
            newKwargs["principal"] = principal   
        if "request" in targetFnArgNames or not targetFnKwargs is None:
            pathParams = event["pathParameters"] if "pathParameters" in event else {}
            queryParams = event["queryStringParameters"] if "queryStringParameters" in event else {}
            requestBody = json.loads(event["body"]) if "body" in event else None
            if requestBody and targetFnSpec.requestBodyType:
                requestBody = ObjectUtil.fromDict(
                    dictValue = requestBody,
                    objectType = targetFnSpec.requestBodyType
                ) 
            request = Request(
                pathParams = pathParams,
                queryParams = queryParams,
                body = requestBody
            )
            self.__logger.info(f"Injecting request with pathParams={pathParams} and queryParams={queryParams} into route handler")
            newKwargs["request"] = request
        self.__logger.info(f"Invoking handler={targetFn} for routeKey={routeKey}")
        try:
            targetFnReturnValue = targetFn(*newVarargs, **newKwargs)
            return self.__generateLambdaResponse(targetFnReturnValue)
        except security.AccessDeniedException:
            return self.__generateLambdaResponse(
                Response(statusCode=403)
            )

    def __generateLambdaResponse(self, response:[object, Response]) -> dict:
        statusCode = 200
        responseBodyObject = response
        if isinstance(response, Response):
            httpResponse:Response = response
            statusCode = httpResponse.statusCode
            responseBodyObject = httpResponse.responseBody
        responseBodyStr = responseBodyObject
        if responseBodyObject and not isinstance(responseBodyObject, str):
            if is_dataclass(responseBodyObject):
                responseBodyStr = ObjectUtil.toJsonStr(asdict(responseBodyObject))
            else:
                responseBodyStr = ObjectUtil.toJsonStr(responseBodyObject)
        return {
            "isBase64Encoded": False,
            "statusCode": statusCode,
            "headers": { 
                "Content-Type": "application/json"
            },
            "body": responseBodyStr
        } 