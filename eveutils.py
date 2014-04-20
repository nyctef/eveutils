import api
import notify
import sched
import logging

class EveUtils(object):
    def __init__(self, clock, api, notify):
        self.scheduler = sched.scheduler(clock.time, clock.sleep)
        self.api = api
        self.notify = notify
        self.scheduler.enter(0, 0, self._do_check, ())

    def run(self):
        self.scheduler.run()
        #print("scheduler ran out of things to do")

    def _do_check(self):
        queue = self.api.get_skill_queue()
        if queue.is_empty:
            self.notify.send('Skill queue empty!', 'Your skill queue is empty!')
        jobs = self.api.get_industry_jobs()
        if jobs.has_deliverable_jobs:
            self.notify.send('Deliverable jobs present!', 'You have some industry jobs which are ready to complete')


if __name__ == '__main__':
    import config
    clock = api.Clock()
    utils = EveUtils(clock, api.EveApi(config, clock), notify.PushBulletNotify(config.pushbullet_api_key))
    utils.run()
