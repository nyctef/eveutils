from api import Clock
import logging
logger = logging.getLogger(__name__)

class SkillQueueChecker(object):
    def __init__(self, api, notify):
        self.api = api
        self.notify = notify
        self.last_result = None

    def _has_changed(self, newqueue, attr):
        if self.last_result is None:
            logger.debug('skipping _has_changed')
            return True
        are_equal = getattr(self.last_result, attr) == getattr(newqueue, attr)
        return not are_equal

    def check(self, sched, reenter=True):
        queue = self.api.get_skill_queue()
        if (queue.is_empty and self._has_changed(queue, "is_empty")):
            self.notify.send('Skill queue empty!', 'Your skill queue is empty!')
        elif (queue.free_time is not None and self._has_changed(queue, "free_time")):
            self.notify.send('Skill queue has space', 'Your skill queue has {} free space'.format(str(queue.free_time)))

        self.last_result = queue
        if reenter:
            from datetime import datetime
            logger.debug('time: '+str(datetime.now()))
            logger.debug('ts: '+str(Clock.timestamp_seconds(datetime.now())))
            logger.debug('cache expires: '+str(queue.cache_expires))
            next_pull_ts = Clock.timestamp_seconds(queue.cache_expires)+10
            logger.debug('next pull ts: '+str(next_pull_ts))
            sched.enterabs(next_pull_ts, 1, self.check, (sched,))
