import os
from datetime import datetime as dt

from _pytest.reports import TestReport

from export_test_jira.models.storage import Storage
from export_test_jira.models.test_cycle import TestCycle

__author__ = 'Dungntc'


class TestCycleService:

    @classmethod
    def create_test_cycle(cls, test_name: str, result: TestReport):
        if result.outcome == 'failed':
            testrun_status = 'Fail'
        else:
            testrun_status = 'Pass'  # and skip
        test_cycle = TestCycle(
            test_name=test_name,
            testrun_status=testrun_status,
            testrun_environment=TestCycleService.get_run_env(),
            testrun_comment=result.capstdout,
            testrun_duration=result.duration,
            testrun_date=dt.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        )
        Storage.list_test_cycle.append(test_cycle)

    @classmethod
    def get_run_env(cls):
        env = os.getenv('CI_COMMIT_BRANCH', '') or os.getenv('ENV', '') or os.getenv('ENVIRONMENT', '')
        env = str(env).lower()
        if not env:
            env = 'local'
        if env == 'master':
            env = 'production'
        if env not in ['local',
                       'test1',
                       'develop', 'dev', 'development',
                       'test', 'testing',
                       'stage', 'staging', 'stg',
                       'pro', 'production']:
            env = 'test1'
        return env
