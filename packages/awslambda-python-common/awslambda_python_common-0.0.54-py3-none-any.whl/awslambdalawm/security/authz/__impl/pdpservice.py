import fnmatch, functools
import boto3
from typing import Union, Tuple, List, Dict, Union
from aws_lambda_powertools import Logger
from awslambdalawm.security.authz.__impl.domain import (
    PdpRequest, ResourceOperation,
    PdpResponse, 
    Policy, PolicyType, SubjectPolicyRule, ResourcePolicyRule, Rule,
    Effect
)
from awslambdalawm.security.authz.__impl.pdprepo import PdpRepo



class PdpService:

    def __init__(self, pdpRepo:PdpRepo):
        self.__pdpRepo = pdpRepo
        self.__logger = Logger()

    def __evaluateResourceOperation(self, resourceOperation:ResourceOperation, 
            subjectUris:List[str], resourcePolicy:Policy, 
            subjectPolicyRules:List[SubjectPolicyRule],
            conditionsContext:Dict) -> PdpResponse:
        def __ruleActionMatched(rule:Rule) -> bool:
            return functools.reduce(
                lambda acc, ruleActionPattern: acc if acc is True else fnmatch.fnmatch(resourceOperation.action, ruleActionPattern),
                rule.actions,
                False
            )
        def __conditionsMatched(rule:Rule) -> bool:
            def __eval_condition(acc:bool, condition:str): 
                if acc is False: # no point proceeding since multiple condition entries are ANDed
                    return acc
                try:
                    return acc and eval(condition, {"__builtins__": {}}, conditionsContext)
                except Exception as e: # any exception will result in False match
                    self.__logger.warning(f"Error evaluation condition in policy rule '{rule}', error={e}")
                    return False
            return functools.reduce(
                __eval_condition,
                rule.conditions,
                True
            )
        # print(f"{resourcePolicy=}")
        resourcePolicyRules = resourcePolicy.rules if not resourcePolicy is None else []
        # print(f"{resourcePolicyRules=}")
        resourceOperationResult = PdpResponse(
            effect = None, 
            obligations = []
        )
        # print(f"{subjectUris=}")
        # print(f"{resourceOperation=}")
        # print(f"{subjectPolicyRules=}")
        for resourcePolicyRule in resourcePolicyRules:
            if resourceOperationResult.effect != Effect.DENY:
                actionMatched = __ruleActionMatched(resourcePolicyRule)
                subjectUriMatched = functools.reduce(
                    lambda acc, ruleSubjectPattern: acc if acc is True else functools.reduce(
                        lambda acc1, subjectUri: acc1 if acc1 is True else fnmatch.fnmatch(subjectUri, ruleSubjectPattern),
                        subjectUris,
                        False 
                    ),
                    resourcePolicyRule.subjects,
                    False
                )
                conditionsMatched = __conditionsMatched(resourcePolicyRule)
                # print(f"in resource policy rule {actionMatched=}, {subjectUriMatched=}, {resourcePolicyRule=}")
                if actionMatched and subjectUriMatched and conditionsMatched:
                    resourceOperationResult = PdpResponse(
                        effect = resourcePolicyRule.effect,
                        obligations = resourceOperationResult.obligations + resourcePolicyRule.obligations
                    )
        # print(f"after resoource policy rule, {resourceOperationResult=}")
        for subjectPolicyRule in subjectPolicyRules:
            if resourceOperationResult.effect != Effect.DENY:
                actionMatched = __ruleActionMatched(subjectPolicyRule)
                resourceUriMatched = functools.reduce(
                    lambda acc, ruleResourcePattern: acc if acc is True else fnmatch.fnmatch(resourceOperation.resourceUri, ruleResourcePattern),
                    subjectPolicyRule.resources,
                    False
                )
                conditionsMatched = __conditionsMatched(subjectPolicyRule)
                # print(f"in subject policies rules {actionMatched=}, {resourceUriMatched=}, {subjectPolicyRule=}")
                if actionMatched and resourceUriMatched and conditionsMatched:
                    resourceOperationResult = PdpResponse(
                        effect = subjectPolicyRule.effect,
                        obligations = resourceOperationResult.obligations + subjectPolicyRule.obligations
                    )
        return resourceOperationResult

    def decide(self, request:PdpRequest) -> PdpResponse:
        subjectUris = request.subjectUris if not request.subjectUris is None else []
        subjectUris = subjectUris if isinstance(subjectUris, list) else [subjectUris]
        resourceOperations = request.resourceOperations
        resourceOperations = resourceOperations if isinstance(resourceOperations, list) else [resourceOperations]
        resourceUris = [
            resourceOperation.resourceUri 
            for resourceOperation in resourceOperations
        ]
        # get all policies that match subject uris or resource uris specified in the list of resource operations
        relevantPolicies:List[Policy] = self.__pdpRepo.getPolicies(subjectUris, resourceUris)
        # print(f"{relevantPolicies=}") 
        resourcePoliciesMap = dict()
        subjectPolicyRules = []
        # for resource policies, create Map of <policy type>-<entity uri> --> Policy
        # for subject policies, extract combined list of rules
        for policy in relevantPolicies:
            if policy.policyType == PolicyType.RESOURCE and policy.entityUri in resourceUris:
                resourcePoliciesMap[f"{policy.policyType.value}-{policy.entityUri}"] = policy
            elif policy.policyType == PolicyType.SUBJECT and policy.entityUri in subjectUris:
                subjectPolicyRules.extend(policy.rules)
        # print(f"{resourcePoliciesMap=}")
        # print(f"{subjectPolicyRules=}")
        resourceOperationsPdpResponseList = [
            self.__evaluateResourceOperation(
                resourceOperation = resourceOperation, 
                subjectUris = subjectUris, 
                resourcePolicy = resourcePoliciesMap[f"{PolicyType.RESOURCE.value}-{resourceOperation.resourceUri}"] if f"{PolicyType.RESOURCE.value}-{resourceOperation.resourceUri}" in resourcePoliciesMap else None,
                subjectPolicyRules = subjectPolicyRules,
                conditionsContext = request.conditionsContext
            )  
            for resourceOperation in resourceOperations
        ]
        # print(f"{resourceOperationsPdpResponseList=}")
        combinedPdpResponse = functools.reduce(
            lambda combinedPdpResponse, resourceOperationResponse: combinedPdpResponse if combinedPdpResponse.effect is Effect.DENY else PdpResponse(
                effect = resourceOperationResponse.effect if not resourceOperationResponse.effect is None else Effect.DENY,
                obligations = [] if resourceOperationResponse.effect is Effect.DENY else combinedPdpResponse.obligations + resourceOperationResponse.obligations
            ),
            resourceOperationsPdpResponseList,
            PdpResponse(
                effect = None,
                obligations = []
            )
        )
        # print(f"{combinedPdpResponse=}")
        return combinedPdpResponse

    def savePolicy(self, policy:Policy) -> Policy:
        self.__logger.info(f"saving policy: {policy}")
        return self.__pdpRepo.savePolicy(policy)

    def getSubjectPolicy(self, subjectUri:str) -> Policy:
        self.__logger.info(f"retrieving subject policy with uri: {subjectUri}")
        return self.__pdpRepo.getSubjectPolicy(subjectUri)

    def getResourcePolicy(self, resourceUri:str) -> Policy:
        self.__logger.info("retrieving resource policy with uri: {resourceUri}")
        return self.__pdpRepo.getResourcePolicy(resourceUri)