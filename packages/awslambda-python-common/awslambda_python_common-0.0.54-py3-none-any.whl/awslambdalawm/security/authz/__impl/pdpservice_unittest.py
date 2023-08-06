from typing import List
import unittest
import unittest.mock as mock
from awslambdalawm.security.authz.__impl.domain import (
    PdpRequest, ResourceOperation, PdpResponse, 
    Policy, PolicyType, Effect,
    ResourcePolicyRule, SubjectPolicyRule
)
from awslambdalawm.security.authz.__impl.pdpservice import PdpService
from awslambdalawm.security.authz.__impl.pdprepo import PdpRepo

@mock.patch(target=f"awslambdalawm.security.authz.__impl.pdprepo.PdpRepo", autospec=True)
class PdpServiceUnitTest(unittest.TestCase):

    def test_decide_resourcePolicy(self, pdprepo:mock.MagicMock):
        pdprepo.getPolicies.return_value = [
            Policy(
                name = "test resource policy",
                entityUri = "resource://projectx/organisation/888",
                policyType = PolicyType.RESOURCE,
                rules = [
                    ResourcePolicyRule(
                        name = "test allow custodian",
                        effect = Effect.ALLOW,
                        subjects = [
                            "subject://projectx/custodian/*",
                        ],
                        actions = [
                            "*"
                        ]
                    ),
                    ResourcePolicyRule(
                        name = "test deny custodian",
                        effect = Effect.DENY,
                        subjects = [
                            "subject://projectx/custodian/*",
                        ],
                        actions = [
                            "notallowedaction"
                        ]
                    ),
                    ResourcePolicyRule(
                        name = "test allow administrator",
                        effect = Effect.ALLOW,
                        subjects = [
                            "subject://projectx/administrator/*",
                        ],
                        actions = [
                            "write"
                        ],
                        obligations = [
                            "obligation3"
                        ]
                    ),
                    ResourcePolicyRule(
                        name = "test allow audience",
                        effect = Effect.ALLOW,
                        subjects = [
                            "subject://projectx/audience/222-222"
                        ],
                        actions = [
                            "read"
                        ],
                        obligations = [
                            "obligation1",
                            "obligation2"
                        ]
                    )
                ]
            )
        ]
        pdpService = PdpService(pdpRepo=pdprepo)
        # subject and action exact match should allow
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = "subject://projectx/audience/222-222",
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = "resource://projectx/organisation/888"
                )
            ), 
            Effect.ALLOW, 
            [
                "obligation1",
                "obligation2"  
            ]
        )
        # subject match but action not matched should deny
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = [
                    "subject://projectx/audience/222-222",
                    "subject://projectx/audience",
                ],
                resourceOperations = ResourceOperation(
                    action = "delete",
                    resourceUri = "resource://projectx/organisation/888"
                )
            ),
            Effect.DENY,
            []
        )
        # subject not matched but action matched should deny
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = "subject://projectx/audience/111-111",
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = "resource://projectx/organisation/888"
                )
            ),
            Effect.DENY,
            []
        )     
        # subject and action wildcard match should allow
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = [
                    "subject://projectx/custodian",
                    "subject://projectx/custodian/zzz"
                ],
                resourceOperations = ResourceOperation(
                    action = "write",
                    resourceUri = "resource://projectx/organisation/888"
                )
            ),
            Effect.ALLOW,
            []
        )  
        # explicit deny should deny
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = "subject://projectx/custodian/zzz",
                resourceOperations = ResourceOperation(
                    action = "notallowedaction",
                    resourceUri = "resource://projectx/organisation/888"
                )
            ),
            Effect.DENY,
            []
        ) 
        # subject wildcard and action exact match should allow
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = "subject://projectx/administrator/zzz",
                resourceOperations = [ResourceOperation(
                    action = "write",
                    resourceUri = "resource://projectx/organisation/888"
                )]
            ),
            Effect.ALLOW,
            [
                "obligation3"
            ]
        )
        # resource not matched should deny
        self.__invoke_decide_and_assert(
            pdpService,
            PdpRequest(
                subjectUris = "subject://projectx/custodian/zzz",
                resourceOperations=ResourceOperation(
                    action = "read",
                    resourceUri = "resource://projectx/organisation/999"
                )
            ),
            Effect.DENY,
            []
        ) 

    def test_decide_subjectPolicy(self, pdprepo:mock.Mock):
        pdprepo.getPolicies.return_value = [
            Policy(
                name = "test subject policy",
                entityUri = "subject://projectx/administrator/111-111",
                policyType = PolicyType.SUBJECT,
                rules = [
                    SubjectPolicyRule(
                        name = "test allow wildcard resource",
                        effect = Effect.ALLOW,
                        resources = [
                            "resource://projectx/resourceType1/*",
                        ],
                        actions = [
                            "read",
                            "write"
                        ]
                    ),
                    SubjectPolicyRule(
                        name = "test deny wildcard resource",
                        effect = Effect.DENY,
                        resources = [
                            "resource://projectx/resourceType1/*",
                        ],
                        actions = [
                            "notallowedaction"
                        ]
                    ),
                    SubjectPolicyRule(
                        name = "test allow wildcard action",
                        effect = Effect.ALLOW,
                        resources = [
                            "resource://projectx/resourceType2/aaa-aaa",
                            "resource://projectx/resourceType2/bbb-bbb",
                        ],
                        actions = [
                            "*"
                        ],
                        obligations = [
                            "obligation3"
                        ]
                    ),
                    SubjectPolicyRule(
                        name = "test allow exact resource and action",
                        effect = Effect.ALLOW,
                        resources = [
                            "resource://projectx/resourceType3/aaa-aaa",
                            "resource://projectx/resourceType3/bbb-bbb",
                        ],
                        actions = [
                            "read"
                        ],
                        obligations = [
                            "obligation1",
                            "obligation2"
                        ]
                    )
                ]
            )
        ]
        pdpService = PdpService(pdpRepo=pdprepo)
        # subject, resource and action exact match should allow
        self.__invoke_decide_and_assert(
            pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/resourceType3/aaa-aaa"
                )
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation1",
                "obligation2"                
            ]
        )
        pdpService = PdpService(pdpRepo=pdprepo)
        # subject, resource exact match, action wildcard match should allow
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "zzzz",
                    "resource://projectx/resourceType2/bbb-bbb"
                ) 
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation3"             
            ]
        )
        pdpService = PdpService(pdpRepo=pdprepo)
        # subject, action exact match, resource wildcard match should allow
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = [
                    "subject://projectx/administrator/111-111",
                    "subject://projectx/custodian"
                ],
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/resourceType1/zzz-zzz"
                )
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = []
        )
        # subject, action exact match, resource wildcard match, deny effect should deny
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = [ResourceOperation(
                    "notallowedaction",
                    "resource://projectx/resourceType1/zzz-zzz"
                )]
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )

    def test_decide_subjectAndResourcePolicy(self, pdprepo:mock.Mock):
        pdprepo.getPolicies.return_value = [
            Policy(
                name = "test subject policy",
                entityUri = "subject://projectx/administrator/111-111",
                policyType = PolicyType.SUBJECT,
                rules = [
                    SubjectPolicyRule(
                        name = "test allow wildcard resource",
                        effect = Effect.ALLOW,
                        resources = [
                            "resource://projectx/resourceType1/*",
                        ],
                        actions = [
                            "read",
                            "write"
                        ],
                        obligations = [
                            "obligation1",
                            "obligation2"
                        ]
                    )
                ]
            ),
            Policy(
                name = "test resource policy",
                entityUri = "resource://projectx/organisation/888",
                policyType = PolicyType.RESOURCE,
                rules = [
                    ResourcePolicyRule(
                        name = "test allow custodian",
                        effect = Effect.ALLOW,
                        subjects = [
                            "subject://projectx/custodian/*",
                        ],
                        actions = [
                            "*"
                        ],
                        obligations = [
                            "obligation3",
                            "obligation4"
                        ]
                    )
                ]
            ),
            Policy(
                name = "test deny resource policy",
                entityUri = "resource://projectx/testexplicitdenyresource/888",
                policyType = PolicyType.RESOURCE,
                rules = [
                    ResourcePolicyRule(
                        name = "test deny administrator",
                        effect = Effect.DENY,
                        subjects = [
                            "subject://projectx/administrator/*",
                        ],
                        actions = [
                            "administratorDeniedAction"
                        ],
                        obligations = []
                    ),
                    ResourcePolicyRule(
                        name = "test allow custodian",
                        effect = Effect.ALLOW,
                        subjects = [
                            "subject://projectx/custodian/*",
                        ],
                        actions = [
                            "administratorDeniedAction"
                        ],
                        obligations = []
                    )
                ]
            )
        ]
        pdpService = PdpService(pdpRepo=pdprepo)
        # subject policy match should allow
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/resourceType1/aaa-aaa"
                )
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation1",
                "obligation2"                
            ]
        )
        # resource policy match should allow
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/custodian/111-111",
                resourceOperations = [ResourceOperation(
                    "some_allowed_operation",
                    "resource://projectx/organisation/888"
                )]
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation3",
                "obligation4"                
            ]
        )
        # resource policy match should allow - multple subject uris
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = [
                    "subject://projectx/blah/111-111",
                    "subject://projectx/custodian/111-111"
                ],
                resourceOperations = [ResourceOperation(
                    "some_allowed_operation",
                    "resource://projectx/organisation/888"
                )]
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation3",
                "obligation4"                
            ]
        )
        # test resource not matched should deny
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "some_allowed_operation",
                    "resource://projectx/organisation/888"
                )
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )
        # test resource not matched should deny - multiple subject uris
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = [
                    "subject://projectx/administrator/111-111",
                    "subject://projectx/blah"
                ],
                resourceOperations = ResourceOperation(
                    "some_allowed_operation",
                    "resource://projectx/organisation/888"
                )
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )
        # test subject not matched should deny
        self.__invoke_decide_and_assert(
            pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/custodian/111-111",
                resourceOperations = ResourceOperation(
                    "some_allowed_operation",
                    "resource://projectx/resourceType1/aaa-aaa"
                )
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )
        # test explicit deny rule but subject allowed should allow 
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/custodian/111-111",
                resourceOperations = ResourceOperation(
                    "administratorDeniedAction",
                    "resource://projectx/testexplicitdenyresource/888"
                )
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = []
        )
       # test explicit deny rule and subject denied should deny 
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "administratorDeniedAction",
                    "resource://projectx/testexplicitdenyresource/888"
                )
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )
       # test explicit deny rule and as long as one subject denied should deny 
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = [
                    "subject://projectx/administrator/111-111",
                    "subject://projectx/custodian/111-111"
                ],
                resourceOperations = ResourceOperation(
                    "administratorDeniedAction",
                    "resource://projectx/testexplicitdenyresource/888"
                )
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )

    def test_decide_subjectAndResourcePolicyWithConditions(self, pdprepo:mock.Mock):
        pdprepo.getPolicies.return_value = [
            Policy(
                name = "test subject policy",
                entityUri = "subject://projectx/administrator/111-111",
                policyType = PolicyType.SUBJECT,
                rules = [
                    SubjectPolicyRule(
                        name = "test allow wildcard resource",
                        effect = Effect.ALLOW,
                        resources = [
                            "resource://projectx/resourceType1/*",
                        ],
                        actions = [
                            "read",
                            "write"
                        ],
                        obligations = [
                            "obligation1",
                            "obligation2"
                        ],
                        conditions = [
                            "contextVar1 is True"
                        ] 
                    )
                ]
            ),
            Policy(
                name = "test resource policy",
                entityUri = "resource://projectx/organisation/888",
                policyType = PolicyType.RESOURCE,
                rules = [
                    ResourcePolicyRule(
                        name = "test allow custodian",
                        effect = Effect.ALLOW,
                        subjects = [
                            "subject://projectx/custodian/*",
                        ],
                        actions = [
                            "*"
                        ],
                        obligations = [
                            "obligation3",
                            "obligation4"
                        ],
                        conditions = [
                            "contextVar1 is False",
                            "contextList1[0] == 'aa'"
                        ]
                    )
                ]
            )
        ]
        pdpService = PdpService(pdpRepo=pdprepo)
        # subject policy condition match should allow
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/resourceType1/aaa-aaa"
                ),
                conditionsContext = {
                    "contextVar1": True
                }
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation1",
                "obligation2"                
            ]
        )
        # subject policy condition UN-matched should deny
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/resourceType1/aaa-aaa"
                ),
                conditionsContext = {
                    "contextVar1": False
                }
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/administrator/111-111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/resourceType1/aaa-aaa"
                ),
                conditionsContext = {}
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )
        # resource policy condition match should allow
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/custodian/111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/organisation/888"
                ),
                conditionsContext = {
                    "contextVar1": False,
                    "contextList1": [ "aa" ]
                }
            ),
            expectedEffect = Effect.ALLOW,
            expectedObligations = [
                "obligation3",
                "obligation4"                
            ]
        )
        # resource policy condition UN-matched should deny
        self.__invoke_decide_and_assert(
            pdpService = pdpService,
            pdpRequest = PdpRequest(
                subjectUris = "subject://projectx/custodian/111",
                resourceOperations = ResourceOperation(
                    "read",
                    "resource://projectx/organisation/888"
                ),
                conditionsContext = {
                    "contextVar1": False,
                    "contextList1": [ "bb" ]
                }
            ),
            expectedEffect = Effect.DENY,
            expectedObligations = []
        )

    def __invoke_decide_and_assert(
        self,
        pdpService:PdpService,
        pdpRequest:PdpRequest, 
        expectedEffect:Effect,
        expectedObligations:List[str]
    ) -> None:
        pdpResponse = pdpService.decide(
            pdpRequest
        )  
        self.assertEqual(pdpResponse.effect, expectedEffect)
        self.assertEqual(pdpResponse.obligations, expectedObligations)

if __name__ == "__main__":
    unittest.main()