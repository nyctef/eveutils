import unittest
from mock import Mock
from datetime import datetime

from evelink.api import APIResult
from api.clock import Clock
from api.industryjobs import IndustryJobs

unfinishedJobs = APIResult(result={218425036: {'status': 'failed', 'delivered': False, 'runs': 50, 'end_ts': 1397080697, 'installer_id': 94534727, 'begin_ts': 1397068737, 'pause_ts': None, 'container_type_id': 57, 'container_id': 60015036, 'activity_id': 1, 'multipliers': {'char_material': 1.25, 'material': 1.0, 'char_time': 0.920000016689301, 'time': 1.0}, 'line_id': 201762, 'finished': False, 'system_id': 30045305, 'output': {'flag': 4, 'bpc_runs': 0, 'location_id': 60015036, 'container_location_id': 30045305, 'type_id': 222}, 'input': {'blueprint_type': 'copy', 'runs_left': 200, 'mat_level': 5, 'prod_level': 2, 'type_id': 1137, 'item_flag': 4, 'location_id': 60015036, 'id': 1014362750679, 'quantity': 1}, 'install_ts': 1397068737}}, timestamp=1397080000, expires=1397082283)
finishedJobs = APIResult(result={218425036: {'status': 'failed', 'delivered': False, 'runs': 50, 'end_ts': 1397080697, 'installer_id': 94534727, 'begin_ts': 1397068737, 'pause_ts': None, 'container_type_id': 57, 'container_id': 60015036, 'activity_id': 1, 'multipliers': {'char_material': 1.25, 'material': 1.0, 'char_time': 0.920000016689301, 'time': 1.0}, 'line_id': 201762, 'finished': False, 'system_id': 30045305, 'output': {'flag': 4, 'bpc_runs': 0, 'location_id': 60015036, 'container_location_id': 30045305, 'type_id': 222}, 'input': {'blueprint_type': 'copy', 'runs_left': 200, 'mat_level': 5, 'prod_level': 2, 'type_id': 1137, 'item_flag': 4, 'location_id': 60015036, 'id': 1014362750679, 'quantity': 1}, 'install_ts': 1397068737}}, timestamp=1397082331, expires=1397083231)
deliveredJobs = APIResult(result={218425036: {'status': 'delivered', 'delivered': True, 'runs': 50, 'end_ts': 1397080697, 'installer_id': 94534727, 'begin_ts': 1397068737, 'pause_ts': None, 'container_type_id': 57, 'container_id': 60015036, 'activity_id': 1, 'multipliers': {'char_material': 1.25, 'material': 1.0, 'char_time': 0.920000016689301, 'time': 1.0}, 'line_id': 201762, 'finished': False, 'system_id': 30045305, 'output': {'flag': 4, 'bpc_runs': 0, 'location_id': 60015036, 'container_location_id': 30045305, 'type_id': 222}, 'input': {'blueprint_type': 'copy', 'runs_left': 200, 'mat_level': 5, 'prod_level': 2, 'type_id': 1137, 'item_flag': 4, 'location_id': 60015036, 'id': 1014362750679, 'quantity': 1}, 'install_ts': 1397068737}}, timestamp=1397085582, expires=1397086482)

def from_ts(timestamp):
    return datetime.fromtimestamp(timestamp)

def clockAtTimeOfRequest(jobsResult):
    clock = Clock()
    clock.now = Mock(return_value=from_ts(jobsResult.timestamp))
    return clock

class ApiTests(unittest.TestCase):

    def testUnfinishedJobsDoNotHaveAnyDeliverableJobs(self):
        clock = clockAtTimeOfRequest(unfinishedJobs)

        jobs = IndustryJobs(unfinishedJobs, clock)

        self.assertFalse(jobs.has_deliverable_jobs)


    def testFinishedJobsDoesHaveADeliverableJob(self):
        clock = clockAtTimeOfRequest(finishedJobs)

        jobs = IndustryJobs(finishedJobs, clock)

        self.assertTrue(jobs.has_deliverable_jobs)

    def testDeliveredJobsDoesNotHaveAnyDeliverableJobs(self):
        clock = clockAtTimeOfRequest(deliveredJobs)

        jobs = IndustryJobs(deliveredJobs, clock)

        self.assertFalse(jobs.has_deliverable_jobs)


            
        
    
