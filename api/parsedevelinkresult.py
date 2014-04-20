import evelink.api
import evelink.eve
import evelink.char
from datetime import datetime

class ParsedEvelinkResult(object):

    def __init__(self, api_result):
        self.api_result = api_result
        self.request_time = datetime.fromtimestamp(request.timestamp)
        self.cache_expires = datetime.fromtimestamp(request.expires)

