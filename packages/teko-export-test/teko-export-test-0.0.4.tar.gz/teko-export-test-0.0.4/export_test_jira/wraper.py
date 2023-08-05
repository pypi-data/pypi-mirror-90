from typing import Optional, List

from export_test_jira.helpers.exception import JiraExportTestException
from export_test_jira.models.test_step import TestStep
from export_test_jira.services.test_case_service import TestCaseService

__author__ = 'Dungntc'


def jira_test(
        test_name: Optional[str] = '',
        issue_links: List[str] = [],
        objective: Optional[str] = '',
        precondition: Optional[str] = '',
        priority: Optional[str] = 'Normal',
        folder: Optional[str] = '',
        web_links: Optional[List[str]] = [],
        confluence_links: Optional[List[str]] = [],
        plan: Optional[str] = '',
        scripts: Optional[List[TestStep]] = []):
    def wrapper(f):
        test_id = f'{f.__name__}-{f.__code__.co_filename}'
        if TestCaseService.find_test_case(test_id=test_id):
            raise JiraExportTestException('Not allow duplicate test function name at same file')
        name = test_name or f.__name__
        name = name.substring(0, 255) if len(name) > 255 else name
        TestCaseService.create_test_case(
            test_id=test_id,
            test_name=name,
            issue_links=issue_links,
            objective=objective,
            precondition=precondition,
            priority=priority,
            folder=folder,
            web_links=web_links,
            confluence_links=confluence_links,
            plan=plan,
            scripts=scripts,
        )
        return f

    return wrapper
