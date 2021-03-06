import eveutils
import unittest
from api import Clock
from mock import Mock
from datetime import datetime, timedelta
from checkers import IndustryJobsChecker, SkillQueueChecker

class Stub(object): pass

class MockClock(Clock):
    def __init__(self, current_time):
        self.current_time = current_time
    def now(self):
        return self.current_time
    def sleep(self, seconds):
        self.current_time = self.current_time + timedelta(seconds=seconds)

class BasicTest(unittest.TestCase):
    def testWhenSkillQueueIsEmptyAMessageIsSent(self):
        queue = self.empty_queue()
        notify = self.mock_notify()
        api = self.mock_api(queue)
        clock = MockClock(datetime.now())

        checkers = (IndustryJobsChecker(api, notify), 
            SkillQueueChecker(api, notify))
        utils = eveutils.EveUtils(clock, checkers)
        utils.run_one()

        notify.send.assert_called_with('le mittani: Skill queue empty!', 'Your skill queue is empty!')

    def mock_api(self, queue=None, jobs=None):
        if queue is None:
            queue = self.empty_queue()
        if jobs is None:
            jobs = self.empty_jobs()
        api = Stub()
        api.get_skill_queue = Mock(return_value=queue)
        api.get_industry_jobs = Mock(return_value=jobs)
        return api

    def empty_jobs(self):
        jobs = Stub()
        jobs.has_deliverable_jobs = False
        return jobs

    def mock_notify(self):
        notify = Stub()
        notify.send = Mock()
        return notify

    def empty_queue(self):
        queue = Stub()
        queue.is_empty = True
        queue.cache_expires = datetime.now() + timedelta(seconds=5)
        queue.free_time = timedelta(hours=24)
        queue.char_name = 'le mittani'
        return queue


if __name__ == '__main__':
    unittest.main()

