from typing import List
import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools.logging import Logger
from awslambdalawm.util import ObjectUtil
from awslambdalawm.security.authz.__impl.domain import Policy, SubjectPolicyRule, ResourcePolicyRule, PolicyType, Effect

class PdpRepo:

    __DYNAMODB_RESOURCE = boto3.resource("dynamodb")

    __DEFAULT_ENTITY_URI_FIELD_NAME = "entityUri"
    __DEFAULT_POLICY_TYPE_FIELD_NAME = "policyType"

    def __init__(self, 
            policiesTableName:str, 
            policiesTableEntityUriFieldName:str = "entityUri",
            policiesTablePolicyTypeFieldName:str = "policyType",
            policiesKeyPrefix:str = ""):
        self.__policiesTableName = policiesTableName
        self.__policiesTableEntityUriFieldName = policiesTableEntityUriFieldName
        self.__policiesTablePolicyTypeFieldName = policiesTablePolicyTypeFieldName
        self.__policiesKeyPrefix = policiesKeyPrefix 
        self.__policiesDdbTableResource = PdpRepo.__DYNAMODB_RESOURCE.Table(policiesTableName)
        self.__logger = Logger()

    def savePolicy(self, policy:Policy) -> None:
        policyDict = ObjectUtil.toDict(policy)
        policyDict[self.__policiesTableEntityUriFieldName] = f"{self.__policiesKeyPrefix}{policy.entityUri}"
        policyDict[self.__policiesTablePolicyTypeFieldName] = f"{self.__policiesKeyPrefix}{policy.policyType}"
        if self.__policiesTableEntityUriFieldName != PdpRepo.__DEFAULT_ENTITY_URI_FIELD_NAME:
            del policyDict[PdpRepo.__DEFAULT_ENTITY_URI_FIELD_NAME]
        if self.__policiesTablePolicyTypeFieldName != PdpRepo.__DEFAULT_POLICY_TYPE_FIELD_NAME:
            del policyDict[PdpRepo.__DEFAULT_POLICY_TYPE_FIELD_NAME]
        self.__policiesDdbTableResource.put_item(
            Item = policyDict
        )
        self.__logger.info(f"savePolicy: saved policy {policyDict}")
        return policy

    def getPolicies(self, subjectUris:List[str], resourceUris:List[str]) -> List[Policy]:
        prefixedUris = [
            f"{self.__policiesKeyPrefix}{resourceUri}"
            for resourceUri in resourceUris
        ]
        policiesDict = PdpRepo.__DYNAMODB_RESOURCE.batch_get_item(
            RequestItems = {
                self.__policiesTableName: {
                    "Keys": [
                        {
                            self.__policiesTableEntityUriFieldName: prefixedUri,
                            self.__policiesTablePolicyTypeFieldName: f"{self.__policiesKeyPrefix}{PolicyType.SUBJECT.value}"
                        } for prefixedUri in prefixedUris
                    ] + [
                        {
                            self.__policiesTableEntityUriFieldName: prefixedUri,
                            self.__policiesTablePolicyTypeFieldName: f"{self.__policiesKeyPrefix}{PolicyType.RESOURCE.value}"
                        } for prefixedUri in prefixedUris
                    ]
                }
            }
        )
        returnPolicies = []
        if self.__policiesTableName in policiesDict["Responses"]:
            policyDicts = policiesDict["Responses"][self.__policiesTableName]
            returnPolicies = [
                ObjectUtil.fromDict(
                    dictValue = {
                        **policyDict, 
                        PdpRepo.__DEFAULT_ENTITY_URI_FIELD_NAME: policyDict[self.__policiesTableEntityUriFieldName].lstrip(self.__policiesKeyPrefix), 
                        PdpRepo.__DEFAULT_POLICY_TYPE_FIELD_NAME: policyDict[self.__policiesTablePolicyTypeFieldName].lstrip(self.__policiesKeyPrefix)
                    },
                    objectType = Policy
                ) for policyDict in policyDicts
            ]
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
        prefixedUris = [
            f"{self.__policiesKeyPrefix}{entityUri}"
            for entityUri in entityUris
        ]
        policiesDict = PdpRepo.__DYNAMODB_RESOURCE.batch_get_item(
            RequestItems = {
                self.__policiesTableName: {
                    "Keys": [
                        {
                            self.__policiesTableEntityUriFieldName: prefixedUri,
                            self.__policiesTablePolicyTypeFieldName: f"{self.__policiesKeyPrefix}{policyType.value}"
                        } for prefixedUri in prefixedUris
                    ]
                }
            }
        )
        returnPolicies=[]
        if self.__policiesTableName in policiesDict["Responses"]:
            policyDicts = policiesDict["Responses"][self.__policiesTableName]
            returnPolicies = [
                ObjectUtil.fromDict(
                    dictValue = {
                        **policyDict,
                        PdpRepo.__DEFAULT_ENTITY_URI_FIELD_NAME: policyDict[self.__policiesTableEntityUriFieldName].lstrip(self.__policiesKeyPrefix),
                        PdpRepo.__DEFAULT_POLICY_TYPE_FIELD_NAME: policyDict[self.__policiesTablePolicyTypeFieldName].lstrip(self.__policiesKeyPrefix),
                    },
                    objectType = Policy
                ) for policyDict in policyDicts
            ]
        self.__logger.info(f"__getPolicies: returning policies {returnPolicies}")
        return returnPolicies

    def __getPolicy(self, entityUri:str, policyType:PolicyType) -> Policy:
        policyDict = self.__policiesDdbTableResource.get_item(
            Key = {
                self.__policiesTableEntityUriFieldName: f"{self.__policiesKeyPrefix}{entityUri}",
                self.__policiesTablePolicyTypeFieldName: f"{self.__policiesKeyPrefix}{policyType.value}"
            }
        )
        returnPolicy = None
        if "Item" in policyDict:
            returnPolicy = ObjectUtil.fromDict(
                dictValue = {
                    **policyDict["Item"],
                    PdpRepo.__DEFAULT_ENTITY_URI_FIELD_NAME: policyDict["Item"][self.__policiesTableEntityUriFieldName].lstrip(self.__policiesKeyPrefix),
                    PdpRepo.__DEFAULT_POLICY_TYPE_FIELD_NAME: policyDict["Item"][self.__policiesTablePolicyTypeFieldName].lstrip(self.__policiesKeyPrefix),
                },
                objectType = Policy
            )
        return returnPolicy

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