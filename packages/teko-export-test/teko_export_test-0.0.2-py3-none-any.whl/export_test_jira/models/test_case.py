from typing import List

from export_test_jira.models.test_step import TestStep

__author__ = 'Dungntc'


class TestCase:
    test_id: int = 0
    test_name: str = ''
    issue_links: List[str] = []
    objective: str = ''
    precondition: str = ''
    priority: str = 'Normal'
    folder: str = ''
    web_links: List[str] = []
    confluence_links: List[str] = []
    plan: str = ''
    scripts: List[TestStep] = []

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        test_case_dict = {
            'name': self.test_name,
            'issueLinks': self.issue_links,
            'objective': self.objective,
            'precondition': self.precondition,
            'priority': self.priority,
            'folder': self.folder,
            'webLinks': self.web_links,
            'confluenceLinks': self.confluence_links,
            'testScript': {}
        }
        if self.plan:
            test_case_dict.update({'testScript': {'type': 'PLAIN_TEXT', 'text': self.plan}})
        if self.scripts:
            scripts = [script.to_dict() for script in self.scripts]
            test_case_dict.update({'testScript': {'type': 'STEP_BY_STEP', 'steps': scripts}})
        return test_case_dict
