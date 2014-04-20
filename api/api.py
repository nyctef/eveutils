import evelink.api
import evelink.eve
import evelink.char
from skillqueue import SkillQueue
from industryjobs import IndustryJobs

class EveApi(object):

    def __init__(self, config, clock):
        self.eve = evelink.eve.EVE()
        self.api = evelink.api.API(api_key=(int(config.eve_api_id), config.eve_api_vcode))
        id_response = self.eve.character_id_from_name(config.char_name)
        self.char = evelink.char.Char(char_id = id_response.result, api=self.api)
        self.clock = clock

    def get_skill_queue(self):
        return SkillQueue(self.char.skill_queue())

    def get_industry_jobs(self):
        return IndustryJobs(self.char.industry_jobs(), self.clock)

