

class IndustryJobsChecker(object):
    def __init__(self, api, notify):
        self.api = api
        self.notify = notify

    def check(self, sched):
        jobs = self.api.get_industry_jobs()
        if jobs.has_deliverable_jobs:
            self.notify.send('Deliverable jobs present!', 'You have some industry jobs which are ready to complete')
