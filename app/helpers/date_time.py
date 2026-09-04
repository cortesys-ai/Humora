from datetime import datetime, timedelta, timezone
import json

class DateTimeHelper:
    def make_epoch(self,row):
        row_dict = row._asdict()
        s = json.dumps(row_dict,default=self.default)
        return json.loads(s,object_hook=self.object_hook)
    
    def default(self,obj):
        if isinstance(obj,datetime):
            timestamp = obj.replace(tzinfo=timezone.utc).timestamp()
            return int(timestamp)

    def object_hook(self, obj):
        _isoformat = obj.get('_isoformat')
        if _isoformat is not None:
            return datetime.fromtimestamp(_isoformat)
        return obj