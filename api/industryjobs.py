import evelink.api
import evelink.char
from clock import Clock

class IndustryJobs(object):

    def __init__(self, api_result, clock):
        self.api_result = api_result
        self.clock = clock
        self.has_deliverable_jobs = False
        for job_id, job in api_result.result.iteritems():
            if job['status'] != 'delivered' and self.clock.is_before_now(job['end_ts']):
                self.has_deliverable_jobs = True
