import evelink.api
import evelink.eve
import evelink.char
from skillqueue import SkillQueue
from industryjobs import IndustryJobs

class EveApi(object):

    def __init__(self, char_name, key, clock):
        self.eve = evelink.eve.EVE()
        self.api = evelink.api.API(api_key=(int(key[0]), key[1]))
        id_response = self.eve.character_id_from_name(char_name)
        self.char = evelink.char.Char(char_id = id_response.result, api=self.api)
        self.clock = clock
        self.char_name = char_name

    def get_skill_queue(self):
        return SkillQueue(self.char_name, self.char.skill_queue())

    def get_industry_jobs(self):
        return IndustryJobs(self.char_name, self.char.industry_jobs(), self.clock)

