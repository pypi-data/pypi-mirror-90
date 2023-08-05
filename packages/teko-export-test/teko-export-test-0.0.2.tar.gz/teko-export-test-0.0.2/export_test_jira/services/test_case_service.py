from export_test_jira.models.storage import Storage
from export_test_jira.models.test_case import TestCase

__author__ = 'Dungntc'


class TestCaseService:

    @classmethod
    def create_test_case(cls, **kwargs):
        test_case = TestCase(**kwargs)
        Storage.list_test_case.append(test_case)

    @classmethod
    def find_test_case(cls, test_id):
        for test_case in Storage.list_test_case:
            if test_case.test_id == test_id:
                return test_case
        return None
