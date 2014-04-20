import evelink.api
import evelink.char
import evelink.eve
from parsedevelinkresult import ParsedEvelinkResult

class SkillQueue(ParsedEvelinkResult):

    def __init__(self, api_result):
        super(IndustryJobs, self).__init__(api_result)
        self.is_empty = False
        if len(self.api_result.result) == 0:
            self.is_empty = True
