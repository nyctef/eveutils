import evelink.api
import evelink.char
import evelink.eve
from parsedevelinkresult import ParsedEvelinkResult
from datetime import datetime, timedelta

class SkillQueue(ParsedEvelinkResult):

    def __init__(self, char_name, api_result):
        super(SkillQueue, self).__init__(api_result)
        self.char_name = char_name
        self.is_paused = False
        self.is_empty = False
        print(api_result)
        if len(self.api_result.result) == 0:
            self.is_empty = True
        queue_end = self.request_time
        for queue_entry in self.api_result.result:
            end_ts = queue_entry['end_ts']
            if end_ts is None:
                self.is_paused = True
                break
            entry_end = datetime.fromtimestamp(end_ts)
            if entry_end > queue_end:
                queue_end = entry_end
        one_day_from_now = self.request_time + timedelta(days=1)
        if queue_end < one_day_from_now:
            self.free_time = (one_day_from_now - queue_end)
        else:
            self.free_time = None
