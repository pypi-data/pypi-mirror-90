import inspect
from dataclasses import dataclass
from typing import List, Tuple, Union, Callable
from aws_lambda_powertools import Logger
from awslambdalawm.security import (
    Principal,
    context
)
from awslambdalawm.security.authz.__impl.domain import (
    ResourceOperation,
    PdpRequest, 
    Effect
)
from awslambdalawm.security.authz.__impl.exception import AccessDeniedException
from awslambdalawm.security.authz.__impl.pdpservice import PdpService



class Pep:

    def __init__(self, pdpService:PdpService):
        self.pdpService = pdpService
        self.__logger = Logger()

    def pep(
        self,
        resourceOperationsGenerator: Callable[..., Union[ResourceOperation, List[ResourceOperation]]],
        subjectUrisGenerator: Callable[..., List[str]] = None,
        conditionsContextGenerator: Callable[..., dict] = None
    ) -> None:
        roGenFullArgSpec = inspect.getfullargspec(resourceOperationsGenerator)
        roGenParams = roGenFullArgSpec.args
        roGenKwargs = roGenFullArgSpec.varkw
        suGenFullArgSpec = inspect.getfullargspec(subjectUrisGenerator) if not subjectUrisGenerator is None else None
        suGeneratorParams = suGenFullArgSpec.args if not subjectUrisGenerator is None else None
        suGeneratorKwargs = suGenFullArgSpec.varkw if not subjectUrisGenerator is None else None
        ccGenFullArgSpec = inspect.getfullargspec(conditionsContextGenerator) if not conditionsContextGenerator is None else None
        ccGeneratorParams = ccGenFullArgSpec.args if not conditionsContextGenerator is None else None
        ccGeneratorKwargs = ccGenFullArgSpec.varkw if not conditionsContextGenerator is None else None
        def wrapper(fn):
            fullArgSpec = inspect.getfullargspec(fn)
            params = fullArgSpec.args
            varargs = fullArgSpec.varargs
            varkwargs = fullArgSpec.varkw
            defaults = fullArgSpec.defaults if not fullArgSpec.defaults is None else [] 
            defaultsLength = len(defaults)
            paramsLength = len(params)
            defaultsMap = {}
            for i, default in enumerate(defaults):
                defaultsMap[params[paramsLength-defaultsLength+i]] = default
            def innerWrapper(*args, **kwargs):
                targetFnKwArgs = {}
                # if target function has no kwargs, we need to filter args to only those expected by the target function
                if varkwargs is None: 
                    for (k,_) in kwargs.items():
                        if k in params:
                            targetFnKwArgs[k] = kwargs[k]
                else: # else its ok to just take in all the kwargs
                    targetFnKwArgs = kwargs.copy()
                generatorKwargs = targetFnKwArgs.copy() if not targetFnKwArgs is None else {}
                argsLength = len(args)
                # first go through all normal parameters
                for i, param in enumerate(params):
                    if i < argsLength:
                        generatorKwargs[param] = args[i]
                    elif param in targetFnKwArgs:
                        generatorKwargs[param] = targetFnKwArgs[param]
                    elif param in defaultsMap:
                        generatorKwargs[param] = defaultsMap[param]
                # next add varargs
                if varargs and argsLength > paramsLength:
                    generatorKwargs[varargs] = tuple(
                        [
                            args[i]
                            for i in range(paramsLength, argsLength)
                        ]
                    )
                if "principal" not in generatorKwargs:
                    generatorKwargs["principal"] = context.getPrincipal() 
                subjectUris = []
                if not subjectUrisGenerator is None:
                    # subject generator kwargs based on the parameters in the function and principal in context
                    subjectGeneratorKwargs = {}
                    if suGeneratorKwargs is None:
                        for param in suGeneratorParams:
                            subjectGeneratorKwargs[param] = generatorKwargs[param]
                    else:
                        subjectGeneratorKwargs = generatorKwargs.copy()
                    subjectUris = subjectUrisGenerator(**subjectGeneratorKwargs)
                else: 
                    # default based on principal in context
                    currentPrincipal:Principal = context.getPrincipal()
                    if not currentPrincipal is None:
                        subjectUris.append(f"subject://{currentPrincipal.tenant}/{currentPrincipal.subjectType}/{currentPrincipal.subjectId}")
                        if not currentPrincipal is None:
                            roles = currentPrincipal.roles
                            for role in roles:
                                subjectUris.append(f"subject://{currentPrincipal.tenant}/role/{role}")
                # resource generator kwargs based on the parameters in the function and principal in context
                resourceOperationsGeneratorKwargs = {}
                if roGenKwargs is None:
                    for param in roGenParams:
                        resourceOperationsGeneratorKwargs[param] = generatorKwargs[param]
                else:
                    resourceOperationsGeneratorKwargs = generatorKwargs.copy()
                resourceOperations = resourceOperationsGenerator(**resourceOperationsGeneratorKwargs)
                # condition context generator kwargs based on parameters in the function and principal in context
                conditionsContext = {}
                if not conditionsContextGenerator is None:
                    conditionsContextGeneratorKwargs = {}
                    if ccGeneratorKwargs is None:
                        for param in ccGeneratorParams:
                            conditionsContextGeneratorKwargs[param] = generatorKwargs[param]
                    else:
                        conditionsContextGeneratorKwargs = generatorKwargs.copy()
                    conditionsContext = conditionsContextGenerator(**conditionsContextGeneratorKwargs)
                pdpRequest = PdpRequest(
                    subjectUris = subjectUris,
                    resourceOperations = resourceOperations,
                    conditionsContext = conditionsContext
                )
                self.__logger.info(pdpRequest)
                pdpResponse = self.pdpService.decide(request = pdpRequest)
                self.__logger.info(pdpResponse)
                if pdpResponse.effect != Effect.ALLOW:
                    raise AccessDeniedException(f"Access denied for {pdpRequest}")
                else:
                    return fn(*args, **targetFnKwArgs)
            return innerWrapper
        return wrapper

