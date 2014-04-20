import unittest
from mock import Mock
from datetime import datetime, timedelta

from evelink.api import APIResult
from api.clock import Clock
from api import IndustryJobs, SkillQueue

unfinished_jobs = APIResult(result={218425036: {'status': 'failed', 'delivered': False, 'runs': 50, 'end_ts': 1397080697, 'installer_id': 94534727, 'begin_ts': 1397068737, 'pause_ts': None, 'container_type_id': 57, 'container_id': 60015036, 'activity_id': 1, 'multipliers': {'char_material': 1.25, 'material': 1.0, 'char_time': 0.920000016689301, 'time': 1.0}, 'line_id': 201762, 'finished': False, 'system_id': 30045305, 'output': {'flag': 4, 'bpc_runs': 0, 'location_id': 60015036, 'container_location_id': 30045305, 'type_id': 222}, 'input': {'blueprint_type': 'copy', 'runs_left': 200, 'mat_level': 5, 'prod_level': 2, 'type_id': 1137, 'item_flag': 4, 'location_id': 60015036, 'id': 1014362750679, 'quantity': 1}, 'install_ts': 1397068737}}, timestamp=1397080000, expires=1397082283)
finished_jobs = APIResult(result={218425036: {'status': 'failed', 'delivered': False, 'runs': 50, 'end_ts': 1397080697, 'installer_id': 94534727, 'begin_ts': 1397068737, 'pause_ts': None, 'container_type_id': 57, 'container_id': 60015036, 'activity_id': 1, 'multipliers': {'char_material': 1.25, 'material': 1.0, 'char_time': 0.920000016689301, 'time': 1.0}, 'line_id': 201762, 'finished': False, 'system_id': 30045305, 'output': {'flag': 4, 'bpc_runs': 0, 'location_id': 60015036, 'container_location_id': 30045305, 'type_id': 222}, 'input': {'blueprint_type': 'copy', 'runs_left': 200, 'mat_level': 5, 'prod_level': 2, 'type_id': 1137, 'item_flag': 4, 'location_id': 60015036, 'id': 1014362750679, 'quantity': 1}, 'install_ts': 1397068737}}, timestamp=1397082331, expires=1397083231)
delivered_jobs = APIResult(result={218425036: {'status': 'delivered', 'delivered': True, 'runs': 50, 'end_ts': 1397080697, 'installer_id': 94534727, 'begin_ts': 1397068737, 'pause_ts': None, 'container_type_id': 57, 'container_id': 60015036, 'activity_id': 1, 'multipliers': {'char_material': 1.25, 'material': 1.0, 'char_time': 0.920000016689301, 'time': 1.0}, 'line_id': 201762, 'finished': False, 'system_id': 30045305, 'output': {'flag': 4, 'bpc_runs': 0, 'location_id': 60015036, 'container_location_id': 30045305, 'type_id': 222}, 'input': {'blueprint_type': 'copy', 'runs_left': 200, 'mat_level': 5, 'prod_level': 2, 'type_id': 1137, 'item_flag': 4, 'location_id': 60015036, 'id': 1014362750679, 'quantity': 1}, 'install_ts': 1397068737}}, timestamp=1397085582, expires=1397086482)
empty_skillqueue = APIResult(result=[], timestamp=1397085582, expires=1397086482)
incomplete_skillqueue = APIResult(result=[{'end_ts': 1398010718, 'level': 5, 'type_id': 3436, 'start_ts': 1397726505, 'end_sp': 256000, 'start_sp': 45255, 'position': 0}], timestamp=1398010717, expires=1398012831)
complete_skillqueue = APIResult(result=[{'end_ts': 1398147995, 'level': 5, 'type_id': 3436, 'start_ts': 1397726505, 'end_sp': 256000, 'start_sp': 45255, 'position': 0}], timestamp=1398010717, expires=1398012831)

def from_ts(timestamp):
    return datetime.fromtimestamp(timestamp)

def clock_at_time_of_request(jobs_result):
    clock = Clock()
    clock.now = Mock(return_value=from_ts(jobs_result.timestamp))
    return clock

class ApiTests(unittest.TestCase):

    def testUnfinishedJobsDoNotHaveAnyDeliverableJobs(self):
        clock = clock_at_time_of_request(unfinished_jobs)

        jobs = IndustryJobs(unfinished_jobs, clock)

        self.assertFalse(jobs.has_deliverable_jobs)


    def testFinishedJobsDoesHaveADeliverableJob(self):
        clock = clock_at_time_of_request(finished_jobs)

        jobs = IndustryJobs(finished_jobs, clock)

        self.assertTrue(jobs.has_deliverable_jobs)

    def testDeliveredJobsDoesNotHaveAnyDeliverableJobs(self):
        clock = clock_at_time_of_request(delivered_jobs)

        jobs = IndustryJobs(delivered_jobs, clock)

        self.assertFalse(jobs.has_deliverable_jobs)

    def testEmptySkillQueueIsEmpty(self):
        queue = SkillQueue(empty_skillqueue)

        self.assertTrue(queue.is_empty)

    def testIncompleteSkillQueueHasFreeTime(self):
        queue = SkillQueue(incomplete_skillqueue)

        self.assertFalse(queue.is_empty)
        #living on the edge - one second to go 
        self.assertEqual(queue.free_time, timedelta(seconds=24*60*60 - 1))

    def testCompleteSkillQueueDoesNotHaveFreeTime(self):
        queue = SkillQueue(complete_skillqueue)

        self.assertFalse(queue.is_empty)
        self.assertEqual(queue.free_time, None)

