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
        self.cache_expires_seconds = Clock.timestamp_seconds(datetime.now()) + (20*60)
        self.queue = Stub()
        self.queue.is_empty = False
        self.queue.is_paused = False
        self.queue.free_time = None
        self.queue.cache_expires = datetime.fromtimestamp(self.cache_expires_seconds)
        self.api.get_skill_queue.return_value = self.queue
        self.longMessage = True

    def test_should_notify_when_skill_queue_is_paused(self):
        self.queue.is_paused = True

        self.checker.check(self.sched)

        self.notify.send.assert_called_with('Skill queue paused!', 'Your skill queue is paused!')

    def test_should_notify_when_skill_queue_is_empty(self):
        self.queue.is_empty = True

        self.checker.check(self.sched)

        self.notify.send.assert_called_with('Skill queue empty!', 'Your skill queue is empty!')

    def test_should_notify_when_skill_queue_has_space(self):
        self.queue.free_time = timedelta(seconds=5)

        self.checker.check(self.sched)

        self.notify.send.assert_called_with('Skill queue has space', 'Your skill queue has 0:00:05 free space')

    def test_should_reschedule_check_for_when_cache_expires(self):
        self.checker.check(self.sched)

        self.sched.enterabs.assert_called_with(self.cache_expires_seconds+10, 1, self.checker.check, (self.sched,))

    def test_should_not_notify_again_until_skill_queue_changes(self):
        self.queue.is_empty = True

        self.checker.check(self.sched)
        self.checker.check(self.sched)

        self.assertEqual(self.notify.send.call_count, 1, "should only be called once")

if __name__ == '__main__':
    unittest.main()
