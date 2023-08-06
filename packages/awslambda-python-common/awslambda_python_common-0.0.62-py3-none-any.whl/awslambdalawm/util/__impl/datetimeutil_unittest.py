import unittest
from datetime import datetime, timezone
import awslambdalawm.util.__impl.datetimeutil as datetimeutil

class DateTimeUtilTest(unittest.TestCase):

    def test_nowUtc(self):
        nowUtc = datetimeutil.nowUtc()
        self.assertIsInstance(nowUtc, datetime)

    def test_fromIso8601Str(self):
        testDateTimeSydneyStr = "2020-10-21T14:31:34+11:00"
        testDateTimeUtcZStr = "2020-10-21T03:31:34Z"
        testDateTimeUtcOffsetStr = "2020-10-21T03:31:34+00:00"
        testDateTimeSydney = datetimeutil.fromIso8601Str(testDateTimeSydneyStr)
        testDateTimeUtcZ = datetimeutil.fromIso8601Str(testDateTimeUtcZStr)
        testDateTimeUtcOffset = datetimeutil.fromIso8601Str(testDateTimeUtcOffsetStr)
        self.assertIsInstance(testDateTimeSydney, datetime)
        self.assertIsInstance(testDateTimeUtcZ, datetime)
        self.assertIsInstance(testDateTimeUtcOffset, datetime)
        self.assertEqual(testDateTimeSydney, testDateTimeUtcOffset)
        self.assertEqual(testDateTimeSydney, testDateTimeUtcZ)

    def test_toIso8601Str(self):
        testDateTime = datetime(
            year = 2020,
            month = 10,
            day = 7,
            hour = 10,
            minute = 35,
            second = 59,
            microsecond = 112000,
            tzinfo=timezone.utc
        )
        testDateTimeStr = datetimeutil.toIso8601Str(testDateTime)
        self.assertEqual(testDateTimeStr, "2020-10-07T10:35:59.112+00:00")

if __name__ == "__main__":
    unittest.main()