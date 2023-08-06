from datetime import datetime, timezone

def nowUtc() -> datetime:
    return datetime.now(tz=timezone.utc)

def toIso8601Str(dt:datetime, timespec:str="milliseconds") -> str:
    return dt.isoformat(timespec=timespec)

def fromIso8601Str(dtStr:str) -> datetime:
    if dtStr.endswith("Z"):
        dtStr = dtStr[0:len(dtStr)-1] + "+00:00"
    return datetime.fromisoformat(dtStr)