from checkers import SkillQueueChecker, IndustryJobsChecker
from mock import Mock
import unittest
from datetime import datetime, timedelta
from api import Clock

class Stub(object): pass

class SkillQueueCheckerTests(unittest.TestCase):

    def setUp(self):
        self.api = Stub()
        self.api.get_skill_queue = Mock()
        self.notify = Stub()
        self.notify.send = Mock()
        self.checker = SkillQueueChecker(self.api, self.notify)
        self.sched = Stub()
        self.sched.enterabs = Mock()

    def test_should_notify_when_skill_queue_is_empty(self):
        queue = Stub()
        queue.is_empty = True
        self.api.get_skill_queue.return_value = queue

        self.checker.check(self.sched)

        self.notify.send.assert_called_with('Skill queue empty!', 'Your skill queue is empty!')

    def test_should_notify_when_skill_queue_has_space(self):
        queue = Stub()
        queue.is_empty = False
        queue.free_time = timedelta(seconds=5)
        self.api.get_skill_queue.return_value = queue

        self.checker.check(self.sched)

        self.notify.send.assert_called_with('Skill queue has space', 'Your skill queue has free space')

    def test_should_reschedule_check_for_when_cache_expires(self):
        queue = Stub()
        queue.is_empty = False
        queue.free_time = timedelta(seconds=5)
        cache_expires_seconds = Clock.timestamp_seconds(datetime.now()) + (20*60)
        queue.cache_expires = datetime.fromtimestamp(cache_expires_seconds)
        self.api.get_skill_queue.return_value = queue

        self.checker.check(self.sched)

        self.sched.enterabs.assert_called_with(cache_expires_seconds, 1, self.checker.check, ())

    def test_should_not_notify_again_until_skill_queue_changes(self):
        queue = Stub()
        queue.is_empty = False
        queue.free_time = timedelta(seconds=5)
        self.api.get_skill_queue.return_value = queue

        self.checker.check(self.sched)

        self.assertEqual(self.notify.send.call_count, 1, "should only be called once")

if __name__ == '__main__':
    unittest.main()
