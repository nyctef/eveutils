from api import Clock

class SkillQueueChecker(object):
    def __init__(self, api, notify):
        self.api = api
        self.notify = notify
        self.last_result = None

    def _has_changed(self, newqueue, attr):
        if self.last_result is None:
            print('skipping _has_changed')
            return True
        are_equal = getattr(self.last_result, attr) == getattr(newqueue, attr)
        return not are_equal

    def check(self, sched, reenter=True):
        queue = self.api.get_skill_queue()
        if (queue.is_empty and self._has_changed(queue, "is_empty")):
            self.notify.send('Skill queue empty!', 'Your skill queue is empty!')
        elif (queue.free_time is not None and self._has_changed(queue, "free_time")):
            self.notify.send('Skill queue has space', 'Your skill queue has free space')

        self.last_result = queue
        if reenter:
            sched.enterabs(Clock.timestamp_seconds(queue.cache_expires)+1, 1, self.check, (sched,))
