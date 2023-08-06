from typing import List, Dict
import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools.logging import Logger
from awslambdalawm.util import ObjectUtil
from awslambdalawm.security.authz.__impl.domain import Policy, SubjectPolicyRule, ResourcePolicyRule, PolicyType, Effect

_DYNAMODB_RESOURCE = boto3.resource("dynamodb")
_DEFAULT_ENTITY_URI_FIELD_NAME = "entityUri"
_DEFAULT_POLICY_TYPE_FIELD_NAME = "policyType"

class PdpRepo:

    def __init__(self, 
            policiesTableName:str, 
            policiesTableEntityUriFieldName:str = _DEFAULT_ENTITY_URI_FIELD_NAME,
            policiesTablePolicyTypeFieldName:str = _DEFAULT_POLICY_TYPE_FIELD_NAME,
            policiesKeyPrefix:str = ""):
        self.__policiesTableName = policiesTableName
        self.__policiesTableEntityUriFieldName = policiesTableEntityUriFieldName
        self.__policiesTablePolicyTypeFieldName = policiesTablePolicyTypeFieldName
        self.__policiesKeyPrefix = policiesKeyPrefix 
        self.__policiesDdbTableResource = _DYNAMODB_RESOURCE.Table(policiesTableName)
        self.__logger = Logger()

    def savePolicy(self, policy:Policy) -> None:
        policyDict = ObjectUtil.toDict(policy)
        policyDict[self.__policiesTableEntityUriFieldName] = self.__prefixKeyFieldValue(policy.entityUri)
        policyDict[self.__policiesTablePolicyTypeFieldName] = self.__prefixKeyFieldValue(policy.policyType)
        if self.__policiesTableEntityUriFieldName != _DEFAULT_ENTITY_URI_FIELD_NAME:
            del policyDict[_DEFAULT_ENTITY_URI_FIELD_NAME]
        if self.__policiesTablePolicyTypeFieldName != _DEFAULT_POLICY_TYPE_FIELD_NAME:
            del policyDict[_DEFAULT_POLICY_TYPE_FIELD_NAME]
        self.__policiesDdbTableResource.put_item(
            Item = policyDict
        )
        self.__logger.info(f"savePolicy: saved policy {policyDict}")
        return policy

    def getPolicies(self, subjectUris:List[str], resourceUris:List[str]) -> List[Policy]:
        batchGetRequestItemsDict = {
            self.__policiesTableName: {
                "Keys": [
                    {
                        self.__policiesTableEntityUriFieldName: prefixedUri,
                        self.__policiesTablePolicyTypeFieldName: self.__prefixKeyFieldValue(PolicyType.SUBJECT.value)
                    } for prefixedUri in self.__prefixEntityUris(subjectUris)
                ] + [
                    {
                        self.__policiesTableEntityUriFieldName: prefixedUri,
                        self.__policiesTablePolicyTypeFieldName: self.__prefixKeyFieldValue(PolicyType.RESOURCE.value)
                    } for prefixedUri in self.__prefixEntityUris(resourceUris)
                ]
            }
        }
        self.__logger.info(f"{batchGetRequestItemsDict=}")
        policiesDict = _DYNAMODB_RESOURCE.batch_get_item(RequestItems = batchGetRequestItemsDict)
        self.__logger.info(f"{policiesDict=}")
        returnPolicies = []
        if self.__policiesTableName in policiesDict["Responses"]:
            policyDicts = policiesDict["Responses"][self.__policiesTableName]
            returnPolicies = self.__policyDictsToPolicies(policyDicts)
        self.__logger.info(f"getPolicies: returning policies {returnPolicies}")
        return returnPolicies

    def getSubjectPolicy(self, subjectUri:str) -> Policy:
        return self.__getPolicy(subjectUri, PolicyType.SUBJECT)

    def getSubjectPolicies(self, subjectUris:List[str]) -> List[Policy]:
        return self.__getPolicies(subjectUris, PolicyType.SUBJECT)

    def getResourcePolicy(self, resourceUri:str) -> Policy:
        return self.__getPolicy(resourceUri, PolicyType.RESOURCE)

    def getResourcePolicies(self, resourceUris:List[str]) -> List[Policy]:
        return self.__getPolicies(resourceUris, PolicyType.RESOURCE)

    def __getPolicies(self, entityUris:List[str], policyType:PolicyType) -> List[Policy]:
        policiesDict = _DYNAMODB_RESOURCE.batch_get_item(
            RequestItems = {
                self.__policiesTableName: {
                    "Keys": [
                        {
                            self.__policiesTableEntityUriFieldName: prefixedUri,
                            self.__policiesTablePolicyTypeFieldName: self.__prefixKeyFieldValue(policyType.value)
                        } for prefixedUri in self.__prefixEntityUris(entityUris)
                    ]
                }
            }
        )
        returnPolicies=[]
        if self.__policiesTableName in policiesDict["Responses"]:
            policyDicts = policiesDict["Responses"][self.__policiesTableName]
            returnPolicies = self.__policyDictsToPolicies(policyDicts)
        self.__logger.info(f"__getPolicies: returning policies {returnPolicies}")
        return returnPolicies

    def __getPolicy(self, entityUri:str, policyType:PolicyType) -> Policy:
        policyDict = self.__policiesDdbTableResource.get_item(
            Key = {
                self.__policiesTableEntityUriFieldName: self.__prefixKeyFieldValue(entityUri),
                self.__policiesTablePolicyTypeFieldName: self.__prefixKeyFieldValue(policyType.value)
            }
        )
        returnPolicy = None
        if "Item" in policyDict:
            returnPolicy = self.__policyDictToPolicy(policyDict["Item"])
        return returnPolicy

    def __policyDictsToPolicies(self, policyDicts:List[Dict]) -> List[Policy]:
        return [
            self.__policyDictToPolicy(policyDict)
            for policyDict in policyDicts
        ] 

    def __policyDictToPolicy(self, policyDict:Dict) -> Policy:
        return ObjectUtil.fromDict(
            dictValue = {
                **policyDict,
                _DEFAULT_ENTITY_URI_FIELD_NAME: self.__unprefixDdbKeyFieldValue(policyDict[self.__policiesTableEntityUriFieldName]),
                _DEFAULT_POLICY_TYPE_FIELD_NAME: self.__unprefixDdbKeyFieldValue(policyDict[self.__policiesTablePolicyTypeFieldName]),
            },
            objectType = Policy
        )

    def __prefixEntityUris(self, entityUris:List[str]) -> List[str]:
        return [
            self.__prefixKeyFieldValue(entityUri)
            for entityUri in entityUris
        ]

    def __prefixKeyFieldValue(self, keyFieldValue:str) -> str:
        return f"{self.__policiesKeyPrefix}{keyFieldValue}"

    def __unprefixDdbKeyFieldValue(self, ddbKeyFieldValue:str) -> str:
        return ddbKeyFieldValue.lstrip(self.__policiesKeyPrefix)

# mySubjectPolicy = Policy(
#     entityUri = "subject://projectx/custodian/111-111",
#     policyType = PolicyType.SUBJECT,
#     rules = [
#         SubjectPolicyRule(
#             effect = Effect.ALLOW,
#             resources = [
#                 "resource://projectx/organisation/*"
#             ],
#             actions = [
#                 "read"
#             ]
#         )
#     ]
# )
# savePolicy(mySubjectPolicy)

# retrievedSubjectPolicy = getSubjectPolicy("subject://projectx/custodian/111-111")
# print(f"{retrievedSubjectPolicy=}")

# myResourcePolicy = Policy(
#     entityUri = "resource://projectx/organisation/888",
#     policyType = PolicyType.RESOURCE,
#     rules = [
#         ResourcePolicyRule(
#             effect = Effect.ALLOW,
#             subjects = [
#                 "subject://projectx/custodian/*",
#                 "subject://projectx/administrator/*"
#             ],
#             actions = [
#                 "*"
#             ]
#         ),
#         ResourcePolicyRule(
#             effect = Effect.ALLOW,
#             subjects = [
#                 "subject://projectx/audience/222-222"
#             ],
#             actions = [
#                 "read"
#             ]
#         )
#     ]
# )
# savePolicy(myResourcePolicy)

# retrievedResourcePolicy = getResourcePolicy("resource://projectx/organisation/888")
# print(f"{retrievedResourcePolicy=}")

# print(getSubjectPolicies(["subject://projectx/custodian/111-111"]))