import unittest
import unittest.mock as mock
from awslambdalawm.security.authz.__impl.pep import Pep
from awslambdalawm.security.authz.__impl.pdpservice import PdpService
from awslambdalawm.security.authz.__impl.domain import ResourceOperation, PdpResponse, Effect, PdpRequest
from awslambdalawm.security import (
    Principal,
    context,
)
from awslambdalawm.security.authz.__impl.exception import AccessDeniedException

@mock.patch(target=f"awslambdalawm.security.authz.__impl.pdpservice.PdpService", autospec=True) 
class PepUnitTest(unittest.TestCase):

    def setUp(self):
       context.setPrincipal(
            Principal(
                clientId = "clientId1",
                subjectType = Principal.SUBJECT_TYPE_USER,
                subjectId = "custodian/111-111",
                tenant = "projectx",
                token = "token1",
                roles = [
                    "audience",
                    "custodian"
                ]
            )
        )

    def test_pep_withVarargsKwargsAndConditionsContext(self, pdpservicemock:mock.MagicMock):
        self.setupPdpserviceMockToReturnAllowed(pdpservicemock)
        pep = Pep(pdpservicemock)
        def subjectUrisGenerator(principal, d, **kwargs):
            self.assertEqual(d, "dd")
            self.assertEqual(principal, context.getPrincipal())
            self.assertTrue(dict(g = "gg", h ="hh", i ="ii").items() <= kwargs.items())
            return f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}"
        def resourceOperationGenerator(principal, a, b, c, d, args):
            self.assertEqual(principal, context.getPrincipal())
            self.assertEqual(a, "aa")
            self.assertEqual(b, "bb")
            self.assertEqual(c, "cc")
            self.assertEqual(d, "dd")
            self.assertTupleEqual(args, ("yy", "zz"))
            return ResourceOperation(
                action = f"read",
                resourceUri = f"resource://{principal.tenant}/organisation/{a}{b}{c}{d}"
            )
        def conditionsContextGenerator(principal, a, b, c, d, args):
            self.assertEqual(principal, context.getPrincipal())
            self.assertEqual(a, "aa")
            self.assertEqual(b, "bb")
            self.assertEqual(c, "cc")
            self.assertEqual(d, "dd")
            self.assertTupleEqual(args, ("yy", "zz"))
            return {
                "contextVar1": "contextVar1-value",
                "contextDict1": {
                    "contextDict1Var1": "contextDict1Var1-value",
                    "contextDict1List1": [ "aaa" ] 
                }
            }    
        @pep.pep(
            subjectUrisGenerator = subjectUrisGenerator,
            resourceOperationsGenerator = resourceOperationGenerator,
            conditionsContextGenerator = conditionsContextGenerator
        )
        def someFunction(a:str, b:str, c:str, d:str, *args, **kwargs):
            pass
        someFunction("aa", "bb", "cc", "dd", "yy", "zz", g = "gg", h ="hh", i ="ii")
        principal = context.getPrincipal()
        pdpservicemock.decide.assert_called_with(
            PdpRequest(
                subjectUris = f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}",
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = f"resource://{principal.tenant}/organisation/aabbccdd"
                ),
                conditionsContext = {
                    "contextVar1": "contextVar1-value",
                    "contextDict1": {
                        "contextDict1Var1": "contextDict1Var1-value",
                        "contextDict1List1": [ "aaa" ] 
                    }
                }    
            )
        )

    def test_pep_defaultSubjectUrisPrincipalInContext(self, pdpservicemock: mock.MagicMock):
        self.setupPdpserviceMockToReturnAllowed(pdpservicemock)
        pep = Pep(pdpservicemock)
        def resourceOperationGenerator(principal, a, b, c, d, args):
            self.assertEqual(principal, context.getPrincipal())
            self.assertEqual(a, "aa")
            self.assertEqual(b, "bb")
            self.assertEqual(c, "cc")
            self.assertEqual(d, "dd")
            self.assertTupleEqual(args, ("yy", "zz"))
            return ResourceOperation(
                action = f"read",
                resourceUri = f"resource://{principal.tenant}/organisation/{a}{b}{c}{d}"
            )
        @pep.pep(
            resourceOperationsGenerator = resourceOperationGenerator
        )
        def someFunction(a:str, b:str, c:str, d:str, *args, **kwargs):
            pass
        someFunction("aa", "bb", "cc", "dd", "yy", "zz", g = "gg", h ="hh", i ="ii")
        principal = context.getPrincipal()
        pdpservicemock.decide.assert_called_with(
            PdpRequest(
                subjectUris = [
                    f"subject://{principal.tenant}/{principal.subjectType}/{principal.subjectId}",
                ] + [
                    f"subject://{principal.tenant}/role/{role}"
                    for role in principal.roles
                ],
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = f"resource://{principal.tenant}/organisation/aabbccdd"
                )
            )
        )

    def test_pep_defaultSubjectUrisPrincipalNotInContext(self, pdpservicemock: mock.MagicMock):
        context.setPrincipal(None)
        self.setupPdpserviceMockToReturnAllowed(pdpservicemock)
        pep = Pep(pdpservicemock)
        def resourceOperationGenerator(a, b, c, d, args):
            self.assertEqual(a, "aa")
            self.assertEqual(b, "bb")
            self.assertEqual(c, "cc")
            self.assertEqual(d, "dd")
            self.assertTupleEqual(args, ("yy", "zz"))
            return ResourceOperation(
                action = f"read",
                resourceUri = f"resource://nothingness/organisation/{a}{b}{c}{d}"
            )
        @pep.pep(
            resourceOperationsGenerator = resourceOperationGenerator
        )
        def someFunction(a:str, b:str, c:str, d:str, *args, **kwargs):
            pass
        someFunction("aa", "bb", "cc", "dd", "yy", "zz", g = "gg", h ="hh", i ="ii")
        pdpservicemock.decide.assert_called_with(
            PdpRequest(
                subjectUris = [],
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = f"resource://nothingness/organisation/aabbccdd"
                )
            )
        )

    def test_pep_withoutVarargsKwargs(self, pdpservicemock: mock.MagicMock):
        self.setupPdpserviceMockToReturnAllowed(pdpservicemock)
        pep = Pep(pdpservicemock)
        def subjectUrisGenerator(principal, d):
            self.assertEqual(d, "dd_default")
            self.assertEqual(principal, context.getPrincipal())
            return f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}"
        def resourceOperationGenerator(principal, a, b, c, d):
            self.assertEqual(principal, context.getPrincipal())
            self.assertEqual(a, "aa")
            self.assertEqual(b, "bb")
            self.assertEqual(c, "cc")
            self.assertEqual(d, "dd_default")
            return ResourceOperation(
                action = f"read",
                resourceUri = f"resource://{principal.tenant}/organisation/{a}{b}{c}{d}"
            )
        @pep.pep(
            subjectUrisGenerator = subjectUrisGenerator,
            resourceOperationsGenerator = resourceOperationGenerator
        )
        def someFunction(a:str, b:str, c:str="cc_default", d:str="dd_default"):
            pass
        someFunction("aa", "bb", "cc")
        principal = context.getPrincipal()
        pdpservicemock.decide.assert_called_with(
            PdpRequest(
                subjectUris = f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}",
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = f"resource://{principal.tenant}/organisation/aabbccdd_default"
                )

            )
        )

    def test_pep_withoutVarargs(self, pdpservicemock: mock.MagicMock):
        self.setupPdpserviceMockToReturnAllowed(pdpservicemock)
        pep = Pep(pdpservicemock)
        def subjectUrisGenerator(principal, a, b, c, **kwargs):
            self.assertEqual(kwargs, dict(d="dd", e="ee"))
            self.assertEqual(principal, context.getPrincipal())
            return f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}"
        def resourceOperationGenerator(principal, a, b, c, d, **kwargs):
            self.assertEqual(principal, context.getPrincipal())
            self.assertEqual(a, "aa")
            self.assertEqual(b, "bb")
            self.assertEqual(c, "cc_default")
            return ResourceOperation(
                action = f"read",
                resourceUri = f"resource://{principal.tenant}/organisation/{a}{b}{c}"
            )
        @pep.pep(
            subjectUrisGenerator = subjectUrisGenerator,
            resourceOperationsGenerator = resourceOperationGenerator
        )
        def someFunction(a:str, b:str, c:str="cc_default", **kwargs):
            pass
        someFunction("aa", b="bb", d="dd", e="ee")
        principal = context.getPrincipal()
        pdpservicemock.decide.assert_called_with(
            PdpRequest(
                subjectUris = f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}",
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = f"resource://{principal.tenant}/organisation/aabbcc_default"
                )

            )
        )

    def test_pep_denied(self, pdpservicemock: mock.MagicMock):
        self.setupPdpserviceMockToReturnDenied(pdpservicemock)
        pep = Pep(pdpservicemock)
        def subjectUrisGenerator(principal, a):
            return f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}"
        def resourceOperationGenerator(principal, a):
            return ResourceOperation(
                action = f"read",
                resourceUri = f"resource://{principal.tenant}/organisation/{a}"
            )
        @pep.pep(
            subjectUrisGenerator = subjectUrisGenerator,
            resourceOperationsGenerator = resourceOperationGenerator
        )
        def someFunction(a:str):
            pass
        self.assertRaises(AccessDeniedException, someFunction, "aa")
        principal = context.getPrincipal()
        pdpservicemock.decide.assert_called_with(
            PdpRequest(
                subjectUris = f"subject://{principal.subjectType}/{principal.tenant}/{principal.subjectId}",
                resourceOperations = ResourceOperation(
                    action = "read",
                    resourceUri = f"resource://{principal.tenant}/organisation/aa"
                )

            )
        )

    def setupPdpserviceMockToReturnAllowed(self, pdpservicemock):
        pdpservicemock.decide.return_value = PdpResponse(
            effect = Effect.ALLOW,
            obligations = [
                "obligation1",
                "obligation2"
            ]
        )

    def setupPdpserviceMockToReturnDenied(self, pdpservicemock):
        pdpservicemock.decide.return_value = PdpResponse(
            effect = Effect.DENY,
            obligations = []
        )

if __name__ == "__main__":
    unittest.main()