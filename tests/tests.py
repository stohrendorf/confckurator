import unittest
from unittest import TestCase

from flask import Response

from server import confckurator

import json


class TestBase(TestCase):
    def setUp(self):
        confckurator.app.config['database'] = 'sqlite:///:memory:'
        confckurator.app.testing = True
        self.app = confckurator.app.test_client()
        with confckurator.app.app_context():
            confckurator.boot_database(confckurator.app)


class BasicTemplateTest(TestBase):
    def test_create_delete(self):
        tpl1 = self.app.post('/api/template', data={
            'name': 'test template',
            'text': 'foo'
        })  # type: Response
        assert tpl1.status_code == 200
        assert tpl1.mimetype == 'application/json'

        tpl1_json = json.loads(tpl1.data)

        assert 'id' in tpl1_json
        tpl1_id = tpl1_json['id']
        assert tpl1_id >= 0

        del1 = self.app.delete('/api/template/{}'.format(tpl1_id))  # type: Response
        assert del1.status_code == 200
        assert del1.mimetype == 'application/json'
        assert json.loads(del1.data) == {}

        del2 = self.app.delete('/api/template/{}'.format(tpl1_id))  # type: Response
        assert del2.status_code >= 300

    def test_duplicate(self):
        tpl1 = self.app.post('/api/template', data={
            'name': 'test template',
            'text': 'foo'
        })  # type: Response
        assert tpl1.status_code == 200
        tpl2 = self.app.post('/api/template', data={
            'name': 'test template',
            'text': 'bar'
        })  # type: Response
        assert tpl2.status_code >= 300

    def test_delete_invalid(self):
        del1 = self.app.delete('/api/template/9999999')  # type: Response
        assert del1.status_code >= 300


if __name__ == "__main__":
    unittest.main()
