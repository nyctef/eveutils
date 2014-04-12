import evelink.api
import evelink.char
import evelink.eve

class SkillQueue(object):

    def __init__(self, api_result):
        self.api_result = api_result
        if len(self.api_result.result) == 0:
            self.is_empty = True
