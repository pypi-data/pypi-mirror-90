import json
from datetime import date, datetime
from enum import Enum
from typing import List, Dict
import dacite
import awslambdalawm.util.__impl.datetimeutil as datetimeutil

def fromDict(dictValue:Dict, objectType:type):
    return dacite.from_dict(
        data_class=objectType,
        data = dictValue,
        config = dacite.Config(
            type_hooks = {
                datetime: datetimeutil.fromIso8601Str,
                date: date.fromisoformat
            },
            cast = [
                Enum
            ]
        )        
    )

def toDict(o:object) -> Dict:
    resultDict = {}
    if "__dict__" in dir(o):
        for k,v in o.__dict__.items():
            if (isinstance(v, datetime)):
                resultDict[k] = datetimeutil.toIso8601Str(v)
            elif (isinstance(v, date)):
                resultDict[k] = v.isoformat()
            elif (isinstance(v, Enum)):
                resultDict[k] = v.name
            elif "__dict__" in dir(v):
                resultDict[k] = toDict(v)
            elif isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set):
                resultDict[k] = []
                for v1 in iter(v):
                    resultDict[k].append(toDict(v1))
            else:
                resultDict[k] = v
        return resultDict 
    else:
        return o

def toJsonStr(obj:object) -> str:
    def default_fn(o):
        if isinstance(o, datetime):
            return datetimeutil.toIso8601Str(o)
        if isinstance(o, date):
            return o.isoformat()
        return o.__dict__
    return json.dumps(
        obj,
        default=default_fn
    )