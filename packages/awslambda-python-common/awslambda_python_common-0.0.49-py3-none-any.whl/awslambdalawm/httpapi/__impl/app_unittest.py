import unittest
import os, json
from datetime import date, datetime, timezone
from dataclasses import dataclass
from typing import Dict, Tuple, List
os.environ["ORGANISATION_NAME"] = "projectx"
os.environ["ACCOUNT_KEY"] = "lmck-dev"
from awslambdalawm.httpapi.__impl.app import App
from awslambdalawm.httpapi.__impl.principalparser import PrincipalParser
from awslambdalawm.httpapi.__impl.domain import RequestMethod, Request, Response
from awslambdalawm.security import Principal, context

class AppTest(unittest.TestCase):

    def setUp(self):
        principalParser = PrincipalParser(
            jwtIdTokenSubjectIdField = "projectx.lmck-dev/userId",
            jwtIdTokenTenantField = "projectx.lmck-dev/tenant",
            jwtIdTokenRolesField = "projectx.lmck-dev/roles",
            jwtSystemAccessTokenScopePrefix = "https://lmck.pawmacy-dev/pawmacy"
        )
        self.app = App(principalParser=principalParser)

    def test_injectEventAndContext_validUser(self):
        event = {
            "routeKey": "POST /v1/test",
            "headers": {
                "authorization": "Bearer eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg"
            }
        }
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST
        )
        def handleRouteRequest(event:Dict, context:Dict):
            return (event, context)
        self.app.handle(event, {})
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 200)
        returnedEvent, returnedContext = json.loads(lambdaResponse["body"])
        self.assertEqual(returnedEvent, event)
        self.assertEqual(returnedContext, {})
        contextPrincipal = context.getPrincipal()
        self.assertIsNotNone(contextPrincipal)
        self.assertEqual(contextPrincipal.clientId, "3jn6jp0hlek9hicrlna8m9s9ua")
        self.assertEqual(contextPrincipal.subjectId, "7f67d9bc-82ce-48fb-9d40-a8cc2a64f213")

    def test_injectPrincipal_validUserPrincipalRequired(self):
        event = {
            "routeKey": "POST /v1/test",
            "headers": {
                "authorization": "Bearer eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg"
            }
        }     
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST,
            principalRequired = True
        )
        def handleRouteRequest(principal:Principal):
            self.assertEqual(principal.clientId, "3jn6jp0hlek9hicrlna8m9s9ua")
            self.assertEqual(principal.subjectType, Principal.SUBJECT_TYPE_USER)
            self.assertEqual(principal.subjectId, "7f67d9bc-82ce-48fb-9d40-a8cc2a64f213")
            self.assertEqual(principal.tenant, "lmck")
            self.assertCountEqual(principal.roles, ["audience"])
            self.assertEqual(principal.token, "eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg")
            return principal
        lambdaResponse = self.app.handle(event, {})
        self.assertIsNotNone(lambdaResponse)
        self.assertEqual(lambdaResponse["statusCode"], 200)
        contextPrincipal = context.getPrincipal()
        self.assertIsNotNone(contextPrincipal)
        self.assertEqual(contextPrincipal.clientId, "3jn6jp0hlek9hicrlna8m9s9ua")
        self.assertEqual(contextPrincipal.subjectId, "7f67d9bc-82ce-48fb-9d40-a8cc2a64f213")
 
    def test_injectPrincipal_validUserPrincipalOptional(self):
        event = {
            "routeKey": "POST /v1/test",
            "headers": {
                "authorization": "Bearer eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg"
            }
        }     
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST,
            principalRequired = False
        )
        def handleRouteRequest(principal:Principal):
            self.assertEqual(principal.clientId, "3jn6jp0hlek9hicrlna8m9s9ua")
            self.assertEqual(principal.subjectType, Principal.SUBJECT_TYPE_USER)
            self.assertEqual(principal.subjectId, "7f67d9bc-82ce-48fb-9d40-a8cc2a64f213")
            self.assertEqual(principal.tenant, "lmck")
            self.assertCountEqual(principal.roles, ["audience"])
            self.assertEqual(principal.token, "eyJraWQiOiJzQlMrbEVNaGF0a1FSMmhSVTNTdkNuc1wvd3J0eWlqMzdNWWlNc0VWSEU5bz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiR013b1JaWlpSS21hcWxtWUxMMS03dyIsInN1YiI6ImZiZGJlYTA3LWVmOTktNGU0NC05NmNkLTk2ZDE0OWFiZTNmNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcm9qZWN0eC5sbWNrLWRldlwvcm9sZXMiOiJhdWRpZW5jZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yb0RxVjFLTnMiLCJjb2duaXRvOnVzZXJuYW1lIjoiZmJkYmVhMDctZWY5OS00ZTQ0LTk2Y2QtOTZkMTQ5YWJlM2Y3IiwicHJvamVjdHgubG1jay1kZXZcL3RlbmFudCI6ImxtY2siLCJhdWQiOiIzam42anAwaGxlazloaWNybG5hOG05czl1YSIsImV2ZW50X2lkIjoiMmMzZDQ2ODMtMDE1OS00ZDljLTgyNDctNTYwMDg4N2MyOGFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDM2Mjc1MzgsInByb2plY3R4LmxtY2stZGV2XC91c2VySWQiOiI3ZjY3ZDliYy04MmNlLTQ4ZmItOWQ0MC1hOGNjMmE2NGYyMTMiLCJjdXN0b206dGVuYW50IjoibG1jayIsImV4cCI6MTYwMzYzMTEzOCwiaWF0IjoxNjAzNjI3NTM5LCJlbWFpbCI6Imxhd3JlbmNlLm1vazc3N0BnbWFpbC5jb20ifQ.hXm7z7pXXNdtShGHjtk5jb0KKFXsLn7h0p5NZKEuvepTdfLgRBcU-VuN8mX6_KAMLr7_wYebQGcYHzweuCKCA-0nQ2aG0v8gTOu11DwDLQ1sEu6xIEuoota9rjUUQr1_1QDyyrHWbSZAf9Sg3kIjI0DGeHYvTqfdJ1f2l9m3ePYa14twYPSyybFM2pvNDhE0Pf_XJ3WGWldl-vl8OSvis6IwqOqggIYfPF2OgT35slaSclfDssVPktn7HKOdeOv6ycQmkKIVyeXaY-Zs6UOxV89h0dYraMp6-jc2daRGi-zWz38-_YSsIEGABFmka5xpa8p6B-fAf3W_ivASn7AiZg")
            return principal
        lambdaResponse = self.app.handle(event, {})
        self.assertIsNotNone(lambdaResponse)
        self.assertEqual(lambdaResponse["statusCode"], 200)
        self.assertIsNotNone(context.getPrincipal())
        contextPrincipal = context.getPrincipal()
        self.assertIsNotNone(contextPrincipal)
        self.assertEqual(contextPrincipal.clientId, "3jn6jp0hlek9hicrlna8m9s9ua")
        self.assertEqual(contextPrincipal.subjectId, "7f67d9bc-82ce-48fb-9d40-a8cc2a64f213")

    def test_injectPrincipal_invalidUserPrincipalRequired(self):
        event = {
            "routeKey": "POST /v1/test",
            "headers": {
                "authorization": "Bearer eyJraWQiOiJGRksycytNdnhhcFl2VkdJQURHNnFiM3dgfdgfdgdfnd3VUQkFJOVwvUXNzc0p5SmlDMD0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzYjA4OGZlMi04OTQ4LTQ5ZTMtOWFmMy0zYmViN2RmZGIxMTEiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl82eThkU0hLVFMiLCJjb2duaXRvOnVzZXJuYW1lIjoiM2IwODhmZTItODk0OC00OWUzLTlhZjMtM2JlYjdkZmRiMTExIiwiYXVkIjoiN2VoNzZrOG0zbHE5azhqdTJkcmpiYmE4aHAiLCJldmVudF9pZCI6ImZlZGE4ZTU1LWQxNGItNDZjOC1hMTNhLWU5NzY2Mzc5NTM5MyIsInByb2plY3R4LnBsYXRmb3JtLWRldlwvdGVuYW50IjoicHJvamVjdHhiMmMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTU5NDI4MzU1MCwicHJvamVjdHgucGxhdGZvcm0tZGV2XC91c2VySWQiOiJiOTIzZmQ5NC03MmQxLTQ5MTEtOTQ1Yy1hNzkzZWZhY2YxOGMiLCJleHAiOjE1OTQyODcxNTAsImlhdCI6MTU5NDI4MzU1MCwiZW1haWwiOiJhQGEuY29tIiwicHJvamVjdHgucGxhdGZvcm0tZGV2XC9yb2xlcyI6ImF1dGhvcixjdXN0b2RpYW4ifQ.bAJ_X859T-SlvXh1RPbg5l88YjYdGz3dQYzV67OWZ22XNrGJ_h2pI5CzR7dWqYeSvHZlWiu9j900c1FiBf2ohuVHG6Ym2mwk4RihFBQ4K6h5Re6cBVsSApTJZVWOFGd4bUwWRzotAscf4QL9inpH8rzyi5wcNPNmTsfcRWo8IC5yNscSWflNT2wPY1NJchSnuAuAqP1YaT2MZjFzmAZZvR70XC3qqklqjgoyWusDodOSbeQQ-QrG_sINNSv1fEuca9BGH-9FTUX98m2x5f79HPFosywc31l3JhEClWBow60SDIazKt8st8dEVI3bJXnN9vqbBz8y3oSIm0qrocH2rw"
            }
        }     
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST,
            principalRequired = True
        )
        def handleRouteRequest(principal:Principal):
            print(f"{principal=}")
            return principal
        lambdaResponse = self.app.handle(event, {})
        self.assertIsNotNone(lambdaResponse)
        self.assertEqual(lambdaResponse["statusCode"], 401)
        self.assertEqual(lambdaResponse["body"], None)
        contextPrincipal = context.getPrincipal()
        self.assertIsNone(contextPrincipal)

    def test_injectPrincipal_invalidUserPrincipalOptional(self):
        event = {
            "routeKey": "POST /v1/test",
            "headers": {
                "authorization": "Bearer eyJraWQiOiJGRksycytNdnhhcFl2VkdJQURHNnFiM3dgfdgfdgdfnd3VUQkFJOVwvUXNzc0p5SmlDMD0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzYjA4OGZlMi04OTQ4LTQ5ZTMtOWFmMy0zYmViN2RmZGIxMTEiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl82eThkU0hLVFMiLCJjb2duaXRvOnVzZXJuYW1lIjoiM2IwODhmZTItODk0OC00OWUzLTlhZjMtM2JlYjdkZmRiMTExIiwiYXVkIjoiN2VoNzZrOG0zbHE5azhqdTJkcmpiYmE4aHAiLCJldmVudF9pZCI6ImZlZGE4ZTU1LWQxNGItNDZjOC1hMTNhLWU5NzY2Mzc5NTM5MyIsInByb2plY3R4LnBsYXRmb3JtLWRldlwvdGVuYW50IjoicHJvamVjdHhiMmMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTU5NDI4MzU1MCwicHJvamVjdHgucGxhdGZvcm0tZGV2XC91c2VySWQiOiJiOTIzZmQ5NC03MmQxLTQ5MTEtOTQ1Yy1hNzkzZWZhY2YxOGMiLCJleHAiOjE1OTQyODcxNTAsImlhdCI6MTU5NDI4MzU1MCwiZW1haWwiOiJhQGEuY29tIiwicHJvamVjdHgucGxhdGZvcm0tZGV2XC9yb2xlcyI6ImF1dGhvcixjdXN0b2RpYW4ifQ.bAJ_X859T-SlvXh1RPbg5l88YjYdGz3dQYzV67OWZ22XNrGJ_h2pI5CzR7dWqYeSvHZlWiu9j900c1FiBf2ohuVHG6Ym2mwk4RihFBQ4K6h5Re6cBVsSApTJZVWOFGd4bUwWRzotAscf4QL9inpH8rzyi5wcNPNmTsfcRWo8IC5yNscSWflNT2wPY1NJchSnuAuAqP1YaT2MZjFzmAZZvR70XC3qqklqjgoyWusDodOSbeQQ-QrG_sINNSv1fEuca9BGH-9FTUX98m2x5f79HPFosywc31l3JhEClWBow60SDIazKt8st8dEVI3bJXnN9vqbBz8y3oSIm0qrocH2rw"
            }
        }     
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST,
            principalRequired = False
        )
        def handleRouteRequest(principal:Principal):
            print(f"{principal=}")
            return principal
        lambdaResponse = self.app.handle(event, {})
        self.assertIsNotNone(lambdaResponse)
        self.assertEqual(lambdaResponse["statusCode"], 200)
        self.assertEqual(lambdaResponse["body"], None)
        contextPrincipal = context.getPrincipal()
        self.assertIsNone(contextPrincipal)

    def test_injectRequest_validRequestNoTypeSpecified(self):
        event = {
            "routeKey": "POST /v1/test",
            "queryStringParameters": {
                "queryParam1": "queryParam1Value1,queryParam1Value2",
                "queryParam2": "queryParam2Value1"
            },
            "pathParameters": {
                "pathParam1": "pathParam1Value"
            },
            "body": """{                
                "bodyField1": "bodyField1Value",
                "bodyField2": 777         
            }"""
        }
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST,
            principalRequired = False
        )
        def handleRouteRequest(request:Request):
            self.assertEqual(request.pathParams, 
                {
                "pathParam1": "pathParam1Value"
                }
            )
            self.assertEqual(request.queryParams, 
                {
                    "queryParam1": "queryParam1Value1,queryParam1Value2",
                    "queryParam2": "queryParam2Value1"
                }
            )
            self.assertIsInstance(request.body, dict)
            self.assertEqual(request.body,
                {
                    "bodyField1": "bodyField1Value",
                    "bodyField2": 777
                }
            )
            return request
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 200)
        self.assertIsNone(context.getPrincipal())

    def test_injectRequest_validRequestWithTypeSpecifiedAndUnknownFieldInPayloadShouldIgnoreUnknownField(self):
        event = {
            "routeKey": "POST /v1/test",
            "queryStringParameters": {
                "queryParam1": "queryParam1Value1,queryParam1Value2",
                "queryParam2": "queryParam2Value1"
            },
            "pathParameters": {
                "pathParam1": "pathParam1Value"
            },
            "body": """{
                "bodyField1": "bodyField1Value",
                "bodyField2": 777,
                "bodyField3": [ "aaa", "bbb" ],
                "unknownField": 888,
                "bodyField4DateTime": "2020-10-07T10:35:59.112Z",
                "bodyField5DateTime": "2020-10-07T10:35:59.112+10:00",
                "bodyField6Date": "2020-10-07",
                "inner": {
                    "innerField1": "innerField1Value1"
                }
            }"""
        }
        @dataclass
        class InnerType:
            innerField1:str
        @dataclass
        class BodyType:
            bodyField1:str
            bodyField2:int
            bodyField3:List[str]
            bodyField4DateTime:datetime
            bodyField5DateTime:datetime
            bodyField6Date: date
            inner: InnerType
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.POST,
            requestBodyType = BodyType,
            principalRequired = False
        )
        def handleRouteRequest(request:Request):
            self.assertEqual(request.pathParams, 
                {
                    "pathParam1": "pathParam1Value"
                }
            )
            self.assertEqual(request.queryParams,
                {
                    "queryParam1": "queryParam1Value1,queryParam1Value2",
                    "queryParam2": "queryParam2Value1"
                }            
            )
            requestBody:BodyType = request.body
            self.assertIsInstance(requestBody, BodyType)
            self.assertEqual(requestBody.bodyField1, "bodyField1Value")
            self.assertEqual(requestBody.bodyField2, 777)
            self.assertEqual(requestBody.bodyField3, ["aaa", "bbb"])
            self.assertEqual(requestBody.bodyField4DateTime, 
                datetime(
                    year = 2020,
                    month = 10,
                    day = 7,
                    hour = 10,
                    minute = 35,
                    second = 59,
                    microsecond = 112000,
                    tzinfo = timezone.utc
                )
            )
            self.assertEqual(requestBody.bodyField5DateTime, 
                datetime(
                    year = 2020,
                    month = 10,
                    day = 7,
                    hour = 0,
                    minute = 35,
                    second = 59,
                    microsecond = 112000,
                    tzinfo = timezone.utc
                )
            )
            self.assertEqual(requestBody.bodyField6Date,
                date(
                    year = 2020,
                    month = 10,
                    day = 7
                )
            )
            self.assertIsInstance(requestBody.inner, InnerType)
            self.assertEqual(requestBody.inner.innerField1, "innerField1Value1")
            return request
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 200)

    def test_returnNormalObject(self):
        event = {
            "routeKey": "GET /v1/test"
        }
        @dataclass
        class ReturnType:
            returnField1:str
            returnField2:datetime
            returnField3:datetime
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.GET,
            principalRequired = False
        )
        def handleRouteRequest(request:Request):
            return ReturnType(
                returnField1 = "value1",
                returnField2 = datetime(
                    year = 2020, 
                    month = 10, 
                    day = 6, 
                    hour = 11, 
                    minute = 17, 
                    second = 23, 
                    microsecond = 0, 
                    tzinfo=timezone.utc
                ),
                returnField3 = date(
                    year = 2020, 
                    month = 10, 
                    day = 7   
                )
            )
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 200)
        lambdaResponseBody = json.loads(lambdaResponse["body"])
        self.assertEqual(lambdaResponseBody["returnField1"], "value1")
        self.assertEqual(lambdaResponseBody["returnField2"], "2020-10-06T11:17:23.000+00:00")
        self.assertEqual(lambdaResponseBody["returnField3"], "2020-10-07")

    def test_returnResponseStrBody(self):
        event = {
            "routeKey": "GET /v1/test"
        }
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.GET,
            principalRequired = False
        )
        def handleRouteRequest(request:Request):
            return Response(201, "aaa")
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 201)
        self.assertEqual(lambdaResponse["body"], "aaa")

    def test_returnResponseObjectBody(self):
        event = {
            "routeKey": "GET /v1/test"
        }
        class ResponseBody:
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.GET,
            principalRequired = False
        )
        def handleRouteRequest(request:Request):
            return Response(
                202,
                ResponseBody(
                    a = "aaa",
                    b = datetime(
                        year = 2020, 
                        month = 10, 
                        day = 6, 
                        hour = 11, 
                        minute = 17, 
                        second = 23, 
                        microsecond = 0, 
                        tzinfo=timezone.utc),
                    c = date(
                        year = 2020,
                        month = 10,
                        day = 7
                    )
                )
            )
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 202)
        lambdaResponseBodyDict = json.loads(lambdaResponse["body"])
        self.assertEqual(lambdaResponseBodyDict["a"], "aaa")
        self.assertEqual(lambdaResponseBodyDict["b"], "2020-10-06T11:17:23.000+00:00")
        self.assertEqual(lambdaResponseBodyDict["c"], "2020-10-07")

    def test_returnResponseDataClassBody(self):
        event = {
            "routeKey": "GET /v1/test"
        }
        @dataclass
        class ResponseBody:
            a:str
            b:datetime
            c:date
        @self.app.route(
            path = "/v1/test",
            method = RequestMethod.GET,
            principalRequired = False
        )
        def handleRouteRequest(request:Request):
            return Response(
                202,
                ResponseBody(
                    a = "aaa",
                    b = datetime(
                        year = 2020, 
                        month = 10, 
                        day = 6, 
                        hour = 11, 
                        minute = 17, 
                        second = 23, 
                        microsecond = 0, 
                        tzinfo=timezone.utc),
                    c = date(
                        year = 2020,
                        month = 10,
                        day = 7
                    )
                )
            )
        lambdaResponse = self.app.handle(event, {})
        self.assertEqual(lambdaResponse["statusCode"], 202)
        lambdaResponseBodyDict = json.loads(lambdaResponse["body"])
        self.assertEqual(lambdaResponseBodyDict["a"], "aaa")
        self.assertEqual(lambdaResponseBodyDict["b"], "2020-10-06T11:17:23.000+00:00")
        self.assertEqual(lambdaResponseBodyDict["c"], "2020-10-07")

if __name__ == "__main__":
    unittest.main()