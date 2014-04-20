

class SkillQueueChecker(object):
    def __init__(self, api, notify):
        self.api = api
        self.notify = notify

    def check(self, sched):
        queue = self.api.get_skill_queue()
        if queue.is_empty:
            self.notify.send('Skill queue empty!', 'Your skill queue is empty!')
