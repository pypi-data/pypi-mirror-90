from typing import List
import boto3
from boto3.dynamodb.conditions import Key
from awslambdalawm.util import ObjectUtil
from awslambdalawm.security.authz.__impl.domain import Policy, SubjectPolicyRule, ResourcePolicyRule, PolicyType, Effect

class PdpRepo:

    __DYNAMODB_RESOURCE = boto3.resource("dynamodb")

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

    def savePolicy(self, policy:Policy) -> None:
        policyDict = ObjectUtil.toDict(policy)
        print(f"{policyDict=}")
        self.__policiesDdbTableResource.put_item(
            Item = policyDict
        )
        return policy

    def getPolicies(self, subjectUris:List[str], resourceUris:List[str]) -> List[Policy]:
        policiesDict = PdpRepo.__DYNAMODB_RESOURCE.batch_get_item(
            RequestItems = {
                self.__policiesTableName: {
                    "Keys": [
                        {
                            self.__policiesTableEntityUriFieldName: subjectUri,
                            self.__policiesTablePolicyTypeFieldName: PolicyType.SUBJECT.value
                        } for subjectUri in subjectUris
                    ] + [
                        {
                            self.__policiesTableEntityUriFieldName: resourceUri,
                            self.__policiesTablePolicyTypeFieldName: PolicyType.RESOURCE.value
                        } for resourceUri in resourceUris
                    ]
                }
            }
        )
        if self.__policiesTableName in policiesDict["Responses"]:
            policyDicts = policiesDict["Responses"][self.__policiesTableName]
            return [
                ObjectUtil.fromDict(
                    dictValue = policyDict,
                    objectType = Policy
                ) for policyDict in policyDicts
            ]
        else:
            return []

    def getSubjectPolicy(self, subjectUri:str) -> Policy:
        return self.__getPolicy(subjectUri, PolicyType.SUBJECT)

    def getSubjectPolicies(self, subjectUris:List[str]) -> List[Policy]:
        return self.__getPolicies(subjectUris, PolicyType.SUBJECT)

    def getResourcePolicy(self, resourceUri:str) -> Policy:
        return self.__getPolicy(resourceUri, PolicyType.RESOURCE)

    def getResourcePolicies(self, resourceUris:List[str]) -> List[Policy]:
        return self.__getPolicies(resourceUris, PolicyType.RESOURCE)

    def __getPolicies(self, entityUris:List[str], policyType:PolicyType) -> List[Policy]:
        policiesDict = PdpRepo.__DYNAMODB_RESOURCE.batch_get_item(
            RequestItems = {
                self.__policiesTableName: {
                    "Keys": [
                        {
                            self.__policiesTableEntityUriFieldName: entityUris,
                            self.__policiesTablePolicyTypeFieldName: policyType.value
                        } for entityUris in entityUris
                    ]
                }
            }
        )
        if self.__policiesTableName in policiesDict["Responses"]:
            policyDicts = policiesDict["Responses"][self.__policiesTableName]
            return [
                ObjectUtil.fromDict(
                    dictValue = policyDict,
                    objectType = Policy
                ) for policyDict in policyDicts
            ]
        else:
            return []

    def __getPolicy(self, entityUri:str, policyType:PolicyType) -> Policy:
        policyDict = self.__policiesDdbTableResource.get_item(
            Key = {
                self.__policiesTableEntityUriFieldName: entityUri,
                self.__policiesTablePolicyTypeFieldName: policyType.value
            }
        )
        if "Item" in policyDict:
            policy = ObjectUtil.fromDict(
                dictValue = policyDict["Item"],
                objectType = Policy
            )
            return policy
        else:
            return None

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