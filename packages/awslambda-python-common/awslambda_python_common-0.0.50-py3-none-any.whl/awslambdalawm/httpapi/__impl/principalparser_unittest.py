import os
import unittest
os.environ["ORGANISATION_NAME"] = "projectx"
os.environ["ACCOUNT_KEY"] = "lmck-dev"
from awslambdalawm.httpapi.__impl.principalparser import PrincipalParser
import awslambdalawm.security as security

class SecurityTest(unittest.TestCase):

    def setUp(self):
        self.__principalParser = PrincipalParser(
            jwtIdTokenSubjectIdField = "projectx.lmck-dev/userId",
            jwtIdTokenTenantField = "projectx.lmck-dev/tenant",
            jwtIdTokenRolesField = "projectx.lmck-dev/roles",
            jwtSystemAccessTokenScopePrefix = "https://lmck.pawmacy-dev"
        )


    def test_getPrincipalFromEvent_validUserPrincipal(self):
        event = {
            "headers": {
                "authorization": "Bearer eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg"
            }
        }
        principal = self.__principalParser.getPrincipalFromEvent(event)
        self.assertIsNotNone(principal)
        self.assertIsInstance(principal, security.Principal)
        self.assertEqual(principal.clientId, "3jn6jp0hlek9hicrlna8m9s9ua")
        self.assertEqual(principal.subjectType, security.Principal.SUBJECT_TYPE_USER)
        self.assertEqual(principal.subjectId, "7f67d9bc-82ce-48fb-9d40-a8cc2a64f213")
        self.assertEqual(principal.tenant, "lmck")
        self.assertCountEqual(principal.roles, ["audience"])
        self.assertEqual(principal.token, "eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg")

    def test_getPrincipalFromEvent_validSystemPrincipal(self):
        event = {
            "headers": {
                "authorization": "Bearer eyJraWQiOiJxdWsxTEhDS2dWY2F4c1lidE5DRHJlVWVPQlNRMUo5N1RpNHJQUVFuYlhzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2N3ZiMG5qZTBxZ2Vta2o3NmRkcDI0NWNuNSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiaHR0cHM6XC9cL2xtY2sucGF3bWFjeS1kZXZcL3Bhd21hY3kiLCJhdXRoX3RpbWUiOjE2MDk2NjM1MTYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl96MWdKN0JrUTUiLCJleHAiOjE2MDk2NjcxMTYsImlhdCI6MTYwOTY2MzUxNiwidmVyc2lvbiI6MiwianRpIjoiMjk0YWJjNWItNGY5Zi00ZDM3LWIyZWQtYWJkNzczZjY3MjNkIiwiY2xpZW50X2lkIjoiNjd2YjBuamUwcWdlbWtqNzZkZHAyNDVjbjUifQ.FCSFm8YgikTl9LKMChJt31a26HNHbQqbnm2wCiYxYphPyOCMz-CdgYFDZ4dyM5O0hUTgkhwMK_XpVKaRwAhXSgM5rKILV3juq4JWJM5lQddMVOa63PiV_RurLMSPH5o27TAQw0YFM3l5M-SXCpLWFLCVskSanJh1J3BTHI_Lw-rfmD0Q2wssw6ZwyANLc1cughliD9x2xYZFrC2dCBFlVUxXnBCsucJ4D6FePZqjiqwfqf6XBe9GJcSRiM88bsG_aARUTOMKjAS2E2aK85QA-srb74gDP4BvrgcFDaMMB33QnBTh-c94ZuR3LaU72l1Il9K3Pup3bP1HNaMB1uReLw"
            }
        }
        principal = self.__principalParser.getPrincipalFromEvent(event)
        self.assertIsNotNone(principal)
        self.assertIsInstance(principal, security.Principal)
        self.assertEqual(principal.clientId, "67vb0nje0qgemkj76ddp245cn5")
        self.assertEqual(principal.subjectType, security.Principal.SUBJECT_TYPE_SYSTEM)
        self.assertEqual(principal.subjectId, "67vb0nje0qgemkj76ddp245cn5")
        self.assertEqual(principal.tenant, "pawmacy")
        self.assertCountEqual(principal.roles, [])
        self.assertEqual(principal.token, "eyJraWQiOiJxdWsxTEhDS2dWY2F4c1lidE5DRHJlVWVPQlNRMUo5N1RpNHJQUVFuYlhzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2N3ZiMG5qZTBxZ2Vta2o3NmRkcDI0NWNuNSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiaHR0cHM6XC9cL2xtY2sucGF3bWFjeS1kZXZcL3Bhd21hY3kiLCJhdXRoX3RpbWUiOjE2MDk2NjM1MTYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl96MWdKN0JrUTUiLCJleHAiOjE2MDk2NjcxMTYsImlhdCI6MTYwOTY2MzUxNiwidmVyc2lvbiI6MiwianRpIjoiMjk0YWJjNWItNGY5Zi00ZDM3LWIyZWQtYWJkNzczZjY3MjNkIiwiY2xpZW50X2lkIjoiNjd2YjBuamUwcWdlbWtqNzZkZHAyNDVjbjUifQ.FCSFm8YgikTl9LKMChJt31a26HNHbQqbnm2wCiYxYphPyOCMz-CdgYFDZ4dyM5O0hUTgkhwMK_XpVKaRwAhXSgM5rKILV3juq4JWJM5lQddMVOa63PiV_RurLMSPH5o27TAQw0YFM3l5M-SXCpLWFLCVskSanJh1J3BTHI_Lw-rfmD0Q2wssw6ZwyANLc1cughliD9x2xYZFrC2dCBFlVUxXnBCsucJ4D6FePZqjiqwfqf6XBe9GJcSRiM88bsG_aARUTOMKjAS2E2aK85QA-srb74gDP4BvrgcFDaMMB33QnBTh-c94ZuR3LaU72l1Il9K3Pup3bP1HNaMB1uReLw")

    def test_getPrincipalFromEvent_invalidToken(self):
        event = {
            "headers": {
                "authorization": "Bearer some_invalid_token"
            }
        }
        with self.assertRaises(Exception):
            self.__principalParser.getPrincipalFromEvent(event)

    def test_getPrincipalFromEvent_noToken(self):
        event = {
            "headers": {
            }
        }
        principal = self.__principalParser.getPrincipalFromEvent(event)
        self.assertIsNone(principal)

    # def test_hasPermissionToAny_forUserPrincipal(self):
    #     test_user_principal = Principal(
    #         clientId = "dont_care",
    #         subjectType = Principal.SUBJECT_TYPE_USER,
    #         subjectId = "dont_care",
    #         tenant = "dont_care",
    #         token = "dont_care",
    #         roles = []
    #     )
    #     self.assertFalse(PermissionsHelper.hasPermissionToAny(test_user_principal))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAny(test_user_principal, "administrator:ccc"))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAny(test_user_principal, "administrator:ccc", "audience"))
    #     # add some roles
    #     test_user_principal.roles = {
    #         "custodian",
    #         "administrator:aaa",
    #         "administrator:bbb"
    #     }
    #     self.assertFalse(PermissionsHelper.hasPermissionToAny(test_user_principal))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAny(test_user_principal, "custodian"))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAny(test_user_principal, "custodian", "audience"))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAny(test_user_principal, "administrator:aaa", "audience"))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAny(test_user_principal, "administrator:ccc", "audience"))
        
    # def test_hasPermissionToAny_forSystemPrincipal(self):
    #     test_system_principal = Principal(
    #         clientId = "dont_care",
    #         subjectType = Principal.SUBJECT_TYPE_SYSTEM,
    #         subjectId = "dont_care",
    #         tenant = "dont_care",
    #         token = "dont_care",
    #         roles = []
    #     )
    #     self.assertTrue(PermissionsHelper.hasPermissionToAny(test_system_principal))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAny(test_system_principal, "administrator:ccc"))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAny(test_system_principal, "administrator:ccc", "audience"))

    # def test_hasPermissionToAll_forUserPrincipal(self):
    #     test_user_principal = Principal(
    #         clientId = "dont_care",
    #         subjectType = Principal.SUBJECT_TYPE_USER,
    #         subjectId = "dont_care",
    #         tenant = "dont_care",
    #         token = "dont_care",
    #         roles = []
    #     )
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_user_principal))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAll(test_user_principal, "administrator:ccc"))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAll(test_user_principal, "administrator:ccc", "audience"))
    #     # add some roles
    #     test_user_principal.roles = {
    #         "custodian",
    #         "administrator:aaa",
    #         "administrator:bbb"
    #     }
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_user_principal))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_user_principal, "custodian"))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_user_principal, "administrator:aaa", "administrator:bbb"))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_user_principal, "administrator:aaa", "custodian", "administrator:bbb"))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAll(test_user_principal, "custodian", "audience"))
    #     self.assertFalse(PermissionsHelper.hasPermissionToAll(test_user_principal, "administrator:aaa", "custodian", "administrator:ccc"))

    # def test_hasPermissionToAll_forSystemPrincipal(self):
    #     test_system_principal = Principal(
    #         clientId = "dont_care",
    #         subjectType = Principal.SUBJECT_TYPE_SYSTEM,
    #         subjectId = "dont_care",
    #         tenant = "dont_care",
    #         token = "dont_care",
    #         roles = []
    #     )
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_system_principal))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_system_principal, "administrator:ccc"))
    #     self.assertTrue(PermissionsHelper.hasPermissionToAll(test_system_principal, "administrator:ccc", "audience"))

if __name__ == "__main__":
    unittest.main()