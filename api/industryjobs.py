import evelink.api
import evelink.char
from clock import Clock
from parsedevelinkresult import ParsedEvelinkResult

class IndustryJobs(ParsedEvelinkResult):

    def __init__(self, char_name, api_result, clock):
        super(IndustryJobs, self).__init__(api_result)
        self.char_name = char_name
        self.clock = clock
        self.has_deliverable_jobs = False
        for job_id, job in api_result.result.iteritems():
            if job['status'] != 'delivered' and self.clock.is_before_now(job['end_ts']):
                self.has_deliverable_jobs = True
