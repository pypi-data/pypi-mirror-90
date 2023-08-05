import json
import os

import pytest

from export_test_jira.helpers.file_io import remove_if_exists, write_file
from export_test_jira.models.storage import Storage
from export_test_jira.services.test_case_service import TestCaseService
from export_test_jira.services.test_cycle_service import TestCycleService

__author__ = 'Dungntc'


@pytest.fixture(scope='function', autouse=True)
def create_test_cycle_after_each_test_function(request):
    test_id = f'{request._pyfuncitem.name}-{request._pyfuncitem.fspath}'
    test_case = TestCaseService.find_test_case(test_id)
    if test_case:
        yield
        TestCycleService.create_test_cycle(test_case.test_name, request.node.result)
    else:
        yield


@pytest.fixture(scope='session', autouse=True)
def generate_test_case_and_test_cycle_file_after_run_all_test():
    test_case_file_path = os.getenv('JIRA_TEST_CASE_ARTIFACT', 'test_case.json')
    test_cycle_file_path = os.getenv('JIRA_TEST_CYCLE_ARTIFACT', 'test_cycle.json')
    remove_if_exists(test_case_file_path)
    remove_if_exists(test_cycle_file_path)
    yield
    test_case = json.dumps(Storage.list_test_case_to_dict(), sort_keys=True, indent=2)
    test_cycle = json.dumps(Storage.list_test_cycle_to_dict(), sort_keys=True, indent=2)
    write_file(test_case_file_path, test_case)
    write_file(test_cycle_file_path, test_cycle)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, 'result', outcome.get_result())
