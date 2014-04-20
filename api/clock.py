from datetime import datetime
import time


class Clock(object):
    """ 
    A wrapper around time-based functions. Should only need 
    now() and sleep() to be mocked out for easy testing
    """
    def time(self):
        return (self.now()-datetime.utcfromtimestamp(0)).total_seconds()

    def sleep(self, seconds):
        time.sleep(seconds)

    def now(self):
        return datetime.now()

    def is_before_now(self, time):
        now = self.now()
        parsed_time = datetime.fromtimestamp(time)
        return (now - parsed_time).total_seconds() > 0

