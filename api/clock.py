from datetime import datetime


class Clock(object):

    def now(self):
        return datetime.now()

    def is_before_now(self, time):
        now = self.now()
        parsed_time = datetime.fromtimestamp(time)
        return (now - parsed_time).total_seconds() > 0

