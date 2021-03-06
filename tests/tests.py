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
        tpl1 = self.app.put('/api/template/', data={
            'name': 'test template',
            'text': 'foo'
        })  # type: Response
        self.assertEqual(tpl1.status_code, 200)
        self.assertEqual(tpl1.mimetype, 'application/json')

        tpl1_json = json.loads(tpl1.data.decode('utf-8'))

        self.assertTrue('id' in tpl1_json)
        tpl1_id = tpl1_json['id']
        self.assertGreaterEqual(tpl1_id, 0)

        del1 = self.app.delete('/api/template/{}'.format(tpl1_id))  # type: Response
        self.assertEqual(del1.status_code, 200)
        self.assertEqual(del1.mimetype, 'application/json')
        self.assertEqual(json.loads(del1.data.decode('utf-8')), {})

        del2 = self.app.delete('/api/template/{}'.format(tpl1_id))  # type: Response
        self.assertEqual(del2.status_code, 404)

    def test_duplicate(self):
        tpl1 = self.app.put('/api/template/', data={
            'name': 'test template',
            'text': 'foo'
        })  # type: Response
        self.assertEqual(tpl1.status_code, 200)
        tpl2 = self.app.put('/api/template/', data={
            'name': 'test template',
            'text': 'bar'
        })  # type: Response
        self.assertEqual(tpl2.status_code, 409)

    def test_delete_invalid(self):
        del1 = self.app.delete('/api/template/9999999')  # type: Response
        self.assertEqual(del1.status_code, 404)


if __name__ == "__main__":
    unittest.main()
