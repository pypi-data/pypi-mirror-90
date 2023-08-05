import re

from export_test_jira.models.storage import Storage
from export_test_jira.models.test_case import TestCase
from export_test_jira.models.test_step import TestStep

__author__ = 'Dungntc'


class TestCaseService:

    @classmethod
    def create_test_case(cls, **kwargs):
        test_case = TestCase(**kwargs)
        Storage.list_test_case.append(test_case)
        return test_case

    @classmethod
    def find_test_case(cls, test_id):
        for test_case in Storage.list_test_case:
            if test_case.test_id == test_id:
                return test_case
        return None

    @classmethod
    def create_test_case_from_docstring(cls, docstring, function_name, test_id):
        MAX_NAME_LENGTH = 255
        if len(function_name) > MAX_NAME_LENGTH:
            function_name = function_name.substring(0, MAX_NAME_LENGTH)
        docstring = docstring + '::END_JIRA'
        scripts = []
        m_scripts_text = TestCaseService.parse_string(docstring, 'scripts:')
        if m_scripts_text:
            for test_step_text in m_scripts_text.split('description:'):
                if 'expectedResult:' and 'testData:' in test_step_text:
                    test_step = TestStep(
                        description=test_step_text[:test_step_text.index('expectedResult:')].strip(),
                        expected_result=test_step_text[test_step_text.index('expectedResult:') + 15
                                                       :test_step_text.index('testData:')].strip(),
                        test_data=test_step_text[test_step_text.index('testData:') + 9:].strip()
                    )
                    scripts.append(test_step)
        test_case = TestCase(
            test_id=test_id,
            test_name=TestCaseService.parse_string(docstring, 'name:', function_name),
            issue_links=TestCaseService.parse_array(docstring, 'issueLinks:'),
            objective=TestCaseService.parse_string(docstring, 'objective:'),
            precondition=TestCaseService.parse_string(docstring, 'precondition:'),
            priority=TestCaseService.parse_string(docstring, 'priority:', 'Normal'),
            folder=TestCaseService.parse_string(docstring, 'folder:'),
            web_links=TestCaseService.parse_array(docstring, 'webLinks:'),
            confluence_links=TestCaseService.parse_array(docstring, 'confluenceLinks:'),
            plan=TestCaseService.parse_string(docstring, 'plan:'),
            scripts=scripts
        )
        Storage.list_test_case.append(test_case)
        return test_case

    @classmethod
    def parse_string(cls, docstring, key, default=''):
        base_regex = '(?s)(.*?)(issueLinks:|objective:|precondition:|priority:' \
                     '|folder:|confluenceLinks:|webLinks:|plan:|scripts:|::END_JIRA)'
        m_key = re.search(key + base_regex, docstring)
        if m_key:
            return m_key.group(1).strip()
        else:
            return default

    @classmethod
    def parse_array(cls, docstring, key, default=[]):
        base_regex = '(?s)(.*?)(issueLinks:|objective:|precondition:|priority:' \
                     '|folder:|confluenceLinks:|webLinks:|plan:|scripts:|::END_JIRA)'
        m_key = re.search(key + base_regex, docstring)
        if m_key:
            return [k.strip() for k in m_key.group(1).split(',')]
        else:
            return default
