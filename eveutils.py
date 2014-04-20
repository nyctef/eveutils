import api
import notify
import sched
import logging
from checkers import IndustryJobsChecker, SkillQueueChecker

class EveUtils(object):
    def __init__(self, clock, checkers):
        # TODO: consider using py3.3's sched since it has a bunch of
        # improvements (nonblocking mode, optional params, etc)
        self.scheduler = sched.scheduler(clock.time, clock.sleep)
        self.scheduler.enter(0, 0, self._start_checks, ())
        self.checkers = checkers

    def run(self):
        self.scheduler.run()

    def _start_checks(self):
        for checker in self.checkers:
            checker.check(self.scheduler)

if __name__ == '__main__':
    import config
    clock = api.Clock()
    api = api.EveApi(config, clock)
    notify = notify.PushBulletNotify(config.pushbullet_api_key)
    checkers = (IndustryJobsChecker(api, notify), 
            SkillQueueChecker(api, notify))
    utils = EveUtils(clock, checkers)
    utils.run()
