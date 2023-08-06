#import time
import datetime
import pytz

class timeconvert:
    def datetime_now_tz(self, tz='Asia/Bangkok'):
        return datetime.datetime.now().astimezone(pytz.timezone(tz))