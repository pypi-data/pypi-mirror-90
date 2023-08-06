import unittest
from datetime import date, datetime, timezone
from dataclasses import dataclass
from awslambdalawm.util.__impl.objectutil import toDict

class ObjectUtilTest(unittest.TestCase):

    def test_toDict_dataClasses(self):
        @dataclass
        class AInnerDataClass:
            aa: str
            bb: datetime
            cc: date
        @dataclass
        class ADataClass:
            a: str
            b: datetime
            c: date
            inner: AInnerDataClass
        aInner = AInnerDataClass(
            aa = "aaaInner",
            bb = datetime(
                year = 2020,
                month = 10,
                day = 7,
                hour = 1,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            cc = date(
                year = 2020,
                month = 10,
                day = 7,
            )
        )
        a = ADataClass(
            a = "aaa",
            b = datetime(
                year = 2020,
                month = 10,
                day = 17,
                hour = 12,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            c = date(
                year = 2020,
                month = 10,
                day = 9,
            ),
            inner = aInner
        )        
        resultDict = toDict(a)
        self.assertEqual(resultDict["a"], "aaa")
        self.assertEqual(resultDict["b"], "2020-10-17T12:13:34.236+00:00")
        self.assertEqual(resultDict["c"], "2020-10-09")
        resultInnerDict = resultDict["inner"]
        self.assertEqual(resultInnerDict["aa"], "aaaInner")
        self.assertEqual(resultInnerDict["bb"], "2020-10-07T01:13:34.236+00:00")
        self.assertEqual(resultInnerDict["cc"], "2020-10-07")

    def test_toDict_normalObjects(self):
        class AInnerDataClass:
            def __init__(self, aa: str, bb: datetime, cc: date):
                self.aa = aa
                self.bb = bb 
                self.cc = cc
        class ADataClass:
            def __init__(self, a: str, b: datetime, c: date, inner: AInnerDataClass):
                self.a = a
                self.b = b 
                self.c = c
                self.inner = inner
        aInner = AInnerDataClass(
            aa = "aaaInner",
            bb = datetime(
                year = 2020,
                month = 10,
                day = 7,
                hour = 1,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            cc = date(
                year = 2020,
                month = 10,
                day = 7,
            )
        )
        a = ADataClass(
            a = "aaa",
            b = datetime(
                year = 2020,
                month = 10,
                day = 17,
                hour = 12,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            c = date(
                year = 2020,
                month = 10,
                day = 9,
            ),
            inner = aInner
        )        
        resultDict = toDict(a)
        print(f"{resultDict=}")
        self.assertEqual(resultDict["a"], "aaa")
        self.assertEqual(resultDict["b"], "2020-10-17T12:13:34.236+00:00")
        self.assertEqual(resultDict["c"], "2020-10-09")
        resultInnerDict = resultDict["inner"]
        self.assertEqual(resultInnerDict["aa"], "aaaInner")
        self.assertEqual(resultInnerDict["bb"], "2020-10-07T01:13:34.236+00:00")
        self.assertEqual(resultInnerDict["cc"], "2020-10-07")

    def test_toDict_outerDataClassInnerNormalObject(self):
        class AInnerDataClass:
            def __init__(self, aa: str, bb: datetime, cc: date):
                self.aa = aa
                self.bb = bb 
                self.cc = cc
        @dataclass
        class ADataClass:
            a: str
            b: datetime
            c: date
            inner: AInnerDataClass
        aInner = AInnerDataClass(
            aa = "aaaInner",
            bb = datetime(
                year = 2020,
                month = 10,
                day = 7,
                hour = 1,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            cc = date(
                year = 2020,
                month = 10,
                day = 7,
            )
        )
        a = ADataClass(
            a = "aaa",
            b = datetime(
                year = 2020,
                month = 10,
                day = 17,
                hour = 12,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            c = date(
                year = 2020,
                month = 10,
                day = 9,
            ),
            inner = aInner
        )        
        resultDict = toDict(a)
        print(f"{resultDict=}")
        self.assertEqual(resultDict["a"], "aaa")
        self.assertEqual(resultDict["b"], "2020-10-17T12:13:34.236+00:00")
        self.assertEqual(resultDict["c"], "2020-10-09")
        resultInnerDict = resultDict["inner"]
        self.assertEqual(resultInnerDict["aa"], "aaaInner")
        self.assertEqual(resultInnerDict["bb"], "2020-10-07T01:13:34.236+00:00")
        self.assertEqual(resultInnerDict["cc"], "2020-10-07")

    def test_toDict_outerNormalObjectInnerDataClass(self):
        @dataclass
        class AInnerDataClass:
            aa: str
            bb: datetime
            cc: date
        class ADataClass:
            def __init__(self, a: str, b: datetime, c: date, inner: AInnerDataClass):
                self.a = a
                self.b = b 
                self.c = c
                self.inner = inner
        aInner = AInnerDataClass(
            aa = "aaaInner",
            bb = datetime(
                year = 2020,
                month = 10,
                day = 7,
                hour = 1,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            cc = date(
                year = 2020,
                month = 10,
                day = 7,
            )
        )
        a = ADataClass(
            a = "aaa",
            b = datetime(
                year = 2020,
                month = 10,
                day = 17,
                hour = 12,
                minute = 13,
                second = 34,
                microsecond = 236000,
                tzinfo=timezone.utc
            ),
            c = date(
                year = 2020,
                month = 10,
                day = 9,
            ),
            inner = aInner
        )        
        resultDict = toDict(a)
        print(f"{resultDict=}")
        self.assertEqual(resultDict["a"], "aaa")
        self.assertEqual(resultDict["b"], "2020-10-17T12:13:34.236+00:00")
        self.assertEqual(resultDict["c"], "2020-10-09")
        resultInnerDict = resultDict["inner"]
        self.assertEqual(resultInnerDict["aa"], "aaaInner")
        self.assertEqual(resultInnerDict["bb"], "2020-10-07T01:13:34.236+00:00")
        self.assertEqual(resultInnerDict["cc"], "2020-10-07")

if __name__ == "__main__":
    unittest.main()